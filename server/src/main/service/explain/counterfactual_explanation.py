import copy
from typing import List

import dice_ml
import pandas as pd
from pymongo import MongoClient
from main.database.explanation_requirement import ExplanationRequirementDb
from main.service.explain.explain import get_training_row, train_decision_tree, encode_categorical_values
from main.service.pre_explanation.data_access import get_labels, get_images, get_masks
import json


class CounterFactualExplanationService:
    explanation_requirement_db: ExplanationRequirementDb

    minimum_counterfactual_probability = [i / 100.0 for i in range(1, 100, 1)]
    minimum_counterfactual_probability.reverse()

    def __init__(self, client: MongoClient):
        self.explanation_requirement_db = ExplanationRequirementDb(client)

    def counterfactual_explanation(self,
                                   explanation_id: str,
                                   to_be_explained_image_index: int,
                                   counter_factual_class: str):

        explanation_requirement = self.explanation_requirement_db.get_explanation_requirement(explanation_id)
        available_concepts = explanation_requirement.available_concepts
        available_concepts.sort()
        if len(available_concepts) == 0:
            raise RuntimeError("Explanation can not be provided, because we can not use any concepts")

        label_encoder, X, y, decision_tree = self.__regular_explain_tree(available_concepts,counter_factual_class)

        # 1. Initialize dice
        dice_explanation = dice_ml.Model(model=decision_tree, backend="sklearn")
        dice_transformed_data = self.__transform_data_for_dice(
            X, y,
            explanation_requirement.available_concepts,
            label_encoder
        )

        dice_data = dice_ml.Data(dataframe=dice_transformed_data,
                                 continuous_features=available_concepts,
                                 outcome_name="label")

        # 2. Initialize the explainer
        exp = dice_ml.Dice(dice_data, dice_explanation, method="genetic")

        # 3. Generate the counterfactual
        to_be_explained_instance = dice_transformed_data.to_dict(orient='records')[to_be_explained_image_index]
        to_be_explained_instance_as_dict = copy.deepcopy(to_be_explained_instance)
        to_be_explained_instance_as_dict["label"] = label_encoder.inverse_transform([to_be_explained_instance_as_dict["label"]])[0]

        original_class = to_be_explained_instance["label"]
        del to_be_explained_instance["label"]
        to_be_explained_instance = pd.DataFrame(to_be_explained_instance, index=[0])

        permitted_range = {concept: [0.0, 1.0] for concept in explanation_requirement.available_concepts}

        error_output = {}
        for minimum_acceptance_probability in self.minimum_counterfactual_probability:
            try:
                counterfactual = exp.generate_counterfactuals(query_instances=to_be_explained_instance,
                                                              total_CFs=1,
                                                              stopping_threshold=minimum_acceptance_probability,
                                                              permitted_range=permitted_range,
                                                              verbose=True,
                                                              desired_class=22).to_json()
                counterfactual = json.loads(counterfactual)
                test_instance_as_array = counterfactual["test_data"][0][0]

                counterfactual_view = []
                for cf_array in counterfactual["cfs_list"][0]:
                    array_diff = [test_instance_as_array[i] - el for i, el in enumerate(cf_array)]
                    dict_diff = {concept: array_diff[i] for i, concept in enumerate(available_concepts)}

                    values = {concept: cf_array[i] for i, concept in enumerate(available_concepts) if
                              cf_array[i] != 0.0}
                    instance = {"values": values, "dif": dict_diff}
                    counterfactual_view.append(instance)

                return {
                    "error": "",
                    "original": {
                        "class": original_class,
                        "values": to_be_explained_instance_as_dict
                    },
                    "counterFactualClass": counter_factual_class,
                    "minimumAcceptanceProbability": minimum_acceptance_probability,
                    "counterfactuals": counterfactual_view,
                }
            except Exception as e:
                print(e, flush=True)
                error_output = {
                    "error": "%s" % e,
                    "original": {
                        "class": original_class,
                        "values": to_be_explained_instance_as_dict
                    },
                    "minimumAcceptanceProbability": minimum_acceptance_probability,
                    "counterFactualClass": counter_factual_class,
                    "counterfactuals": [],
                }
        return error_output

    @staticmethod
    def __transform_data_for_dice(X, y, concepts: List[str],label_encoder):
        data = {}
        for x_i, y_i in zip(X, y):
            current_y_values = data.get("label", [])
            #current_y_values.append(label_encoder.inverse_transform([y_i])[0])
            current_y_values.append(y_i)
            data["label"] = current_y_values

            for i, c in enumerate(concepts):
                current_c_values = data.get(c, [])
                current_c_values.append(x_i[i])
                data[c] = current_c_values
        return pd.DataFrame(data=data)

    @staticmethod
    def __regular_explain_tree(available_concepts: List[str],counter_factual_class: str):
        label_encoder = encode_categorical_values(get_labels())
        X, y = [], []
        numer_of_instances_with_counterfactual = 0
        for label, pic, mask in zip(get_labels(), get_images(), get_masks()):
            row = get_training_row(available_concepts, pic, mask)
            label_as_nr = int(label_encoder.transform([label])[0])
            y.append(label_as_nr)
            X.append(row)
            if label == counter_factual_class:
                numer_of_instances_with_counterfactual += 1

        print("Number of instances with counterfactual: %d" % numer_of_instances_with_counterfactual, flush=True)
        print("Number of instances: %d" % len(y), flush=True)


        clf = train_decision_tree(X, y)
        return label_encoder, X, y, clf

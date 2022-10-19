import copy
from typing import List

import dice_ml
import pandas as pd
from pymongo import MongoClient
from main.database.explanation_requirement import ExplanationRequirementDb
from main.service.explain.explain import get_training_row, train_decision_tree
from main.service.pre_explanation.data_access import get_labels, get_images, get_masks
import json


class CounterFactualExplanationService:
    explanation_requirement_db: ExplanationRequirementDb

    def __init__(self, client: MongoClient):
        self.explanation_requirement_db = ExplanationRequirementDb(client)

    def counterfactual_explanation(self,
                                   explanation_id: str,
                                   to_be_explained_image_index: int,
                                   counter_factual_class: str):

        explanation_requirement = self.explanation_requirement_db.get_explanation_requirement(explanation_id)
        available_concepts = explanation_requirement.available_concepts
        available_concepts.sort()

        """TODO we should not use binary explanations"""
        X, y, decision_tree = self.__binary_explain_tree(
            available_concepts,
            counter_factual_class)

        # 1. Initialize dice
        dice_explanation = dice_ml.Model(model=decision_tree, backend="sklearn")
        dice_transformed_data = self.__transform_data_for_dice(
            X, y,
            available_concepts,
        )

        dice_data = dice_ml.Data(dataframe=dice_transformed_data,
                                 continuous_features=available_concepts,
                                 outcome_name="label")

        # 2. Initialize the explainer
        exp = dice_ml.Dice(dice_data, dice_explanation, method="genetic")

        # 3. Generate the counterfactual
        to_be_explained_instance = dice_transformed_data.to_dict(orient='records')[to_be_explained_image_index]
        to_be_explained_instance_as_dict = copy.deepcopy(to_be_explained_instance)

        original_class = to_be_explained_instance["label"]
        del to_be_explained_instance["label"]
        to_be_explained_instance = pd.DataFrame(to_be_explained_instance, index=[0])

        try:
            permitted_range = {concept: [0.0, 1.0] for concept in explanation_requirement.available_concepts}

            counterfactual = exp.generate_counterfactuals(query_instances=to_be_explained_instance,
                                                          total_CFs=2,
                                                          stopping_threshold=0.01,
                                                          permitted_range=permitted_range,
                                                          verbose=True,
                                                          desired_class="opposite").to_json()
            counterfactual = json.loads(counterfactual)
            test_instance_as_array = counterfactual["test_data"][0][0]

            counterfactualView = []
            for cf_array in counterfactual["cfs_list"][0]:
                array_diff = [test_instance_as_array[i] - el for i, el in enumerate(cf_array)]
                dict_diff = {concept: array_diff[i] for i, concept in enumerate(available_concepts)}

                values = {concept: cf_array[i] for i, concept in enumerate(available_concepts) if cf_array[i] != 0.0}
                instance = {"values": values, "dif": dict_diff}
                counterfactualView.append(instance)

            return {
                "error": "",
                "original": {
                    "class": original_class,
                    "values": to_be_explained_instance_as_dict
                },
                "counterFactualClass": counter_factual_class,
                "counterfactuals": counterfactualView,
            }
        except Exception as e:
            return {
                "error": "%s" % e,
                "original": {
                    "class": original_class,
                    "values": to_be_explained_instance_as_dict
                },
                "counterFactualClass": counter_factual_class,
                "counterfactuals": [],
            }

    @staticmethod
    def __transform_data_for_dice(X, y, concepts: List[str]):
        data = {}
        for x_i, y_i in zip(X, y):
            current_y_values = data.get("label", [])
            current_y_values.append(y_i)
            data["label"] = current_y_values

            for i, c in enumerate(concepts):
                current_c_values = data.get(c, [])
                current_c_values.append(x_i[i])
                data[c] = current_c_values
        return pd.DataFrame(data=data)

    @staticmethod
    def __binary_explain_tree(available_concepts: List[str], counter_factual_class: str):
        if len(available_concepts) == 0:
            raise RuntimeError("Explanation can not be provided, because we can not use any concepts")

        X, y = [], []
        for label, pic, mask in zip(get_labels(), get_images(), get_masks()):
            y_i = 1
            if label == counter_factual_class:
                y_i = 0
            row = get_training_row(available_concepts, pic, mask)
            X.append(row)
            y.append(y_i)

        print("Number of training examples: %d" % len(X), flush=True)
        print("Number of training examples with label 0: %d" % len([y_i for y_i in y if y_i == 0]), flush=True)
        print("Number of training examples with label 1: %d" % len([y_i for y_i in y if y_i == 1]), flush=True)

        clf = train_decision_tree(X, y)
        return X, y, clf

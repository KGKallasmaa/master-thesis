import copy
from typing import List

import dice_ml
import pandas as pd

from main.database.closest_labels import ClosestLabelsDb
from main.database.explanation_requirement import ExplanationRequirementDb
from main.service.explain.explain import get_training_row, train_decision_tree, encode_categorical_values
from main.service.pre_explanation.data_access import get_labels, get_images, get_masks
import json

closest_label_db = ClosestLabelsDb()
explanation_requirement_db = ExplanationRequirementDb()

COUNTERFACTUAL_LABEL = 1
ORIGINAL = 0

minimum_counterfactual_probability = [i / 100.0 for i in range(25, 101, 1)]
minimum_counterfactual_probability.reverse()


class CounterFactualExplanationService:

    def counterfactual_explanation(self,
                                   explanation_id: str,
                                   to_be_explained_image_index: int,
                                   counter_factual_class: str):

        explanation_requirement = explanation_requirement_db.get_explanation_requirement(explanation_id)
        user_specified_concepts = explanation_requirement.user_specified_concepts
        if len(user_specified_concepts) == 0:
            raise RuntimeError("Explanation can not be provided, because we can not use any concepts")

        X, y, black_box_model = self.__find_blackbox_model(user_specified_concepts,
                                                           counter_factual_class,
                                                           to_be_explained_image_index)

        # 1. Initialize dice
        dice_explanation = dice_ml.Model(model=black_box_model, backend="sklearn")
        dice_transformed_data = self.__transform_data_for_dice(X, y, user_specified_concepts)

        dice_data = dice_ml.Data(dataframe=dice_transformed_data,
                                 continuous_features=user_specified_concepts,
                                 outcome_name="label")

        # 2. Initialize the explainer
        exp = dice_ml.Dice(dice_data, dice_explanation, method="genetic")

        # 3. Generate the counterfactual
        to_be_explained_instance = dice_transformed_data.to_dict(orient='records')[to_be_explained_image_index]
        to_be_explained_instance_as_dict = copy.deepcopy(to_be_explained_instance)
        del to_be_explained_instance["label"]

        to_be_explained_instance = pd.DataFrame(to_be_explained_instance, index=[0])

        permitted_range = {concept: [0.0, 1.0] for concept in explanation_requirement.user_specified_concepts}

        error_output = {}
        for minimum_acceptance_probability in minimum_counterfactual_probability:
            try:
                counterfactual = exp.generate_counterfactuals(query_instances=to_be_explained_instance,
                                                              total_CFs=2,
                                                              stopping_threshold=minimum_acceptance_probability,
                                                              permitted_range=permitted_range,
                                                              verbose=True,
                                                              desired_class=COUNTERFACTUAL_LABEL).to_json()
                counterfactual = json.loads(counterfactual)
                test_instance_as_array = counterfactual["test_data"][0][0]

                counterfactual_view = []
                for cf_array in counterfactual["cfs_list"][0]:
                    array_diff = [test_instance_as_array[i] - el for i, el in enumerate(cf_array)]
                    dict_diff = {concept: array_diff[i] for i, concept in enumerate(user_specified_concepts)}

                    values = {concept: cf_array[i] for i, concept in enumerate(user_specified_concepts)}
                    instance = {"values": values, "dif": dict_diff}
                    counterfactual_view.append(instance)

                return {
                    "error": "",
                    "original": {
                        "class": get_labels()[to_be_explained_image_index],
                        "values": to_be_explained_instance_as_dict
                    },
                    "counterFactualClass": counter_factual_class,
                    "minimumAcceptanceProbability": minimum_acceptance_probability,
                    "counterfactuals": counterfactual_view,
                }
            except Exception as e:
                error_output = {
                    "error": "%s" % e,
                    "original": {
                        "class": get_labels()[to_be_explained_image_index],
                        "values": to_be_explained_instance_as_dict
                    },
                    "minimumAcceptanceProbability": minimum_acceptance_probability,
                    "counterFactualClass": counter_factual_class,
                    "counterfactuals": [],
                }
        return error_output

    @staticmethod
    def __transform_data_for_dice(X, y, concepts: List[str]):
        data = {}
        for x_i, y_i in zip(X, y):
            data["label"] = data.get("label", []) + [y_i]
            for i, c in enumerate(concepts):
                data[c] = data.get(c, []) + [x_i[i]]
        return pd.DataFrame(data=data)

    @staticmethod
    def __find_blackbox_model(available_concepts: List[str], counter_factual_class: str,
                              to_be_explained_image_index: int):
        closest = closest_label_db.get_by_image_id(to_be_explained_image_index)
        valid_labels = [closest.label] + [counter_factual_class] + closest.closest

        label_encoder = encode_categorical_values(get_labels())
        X, y = [], []

        for label, pic, mask in zip(get_labels(), get_images(), get_masks()):
            row = get_training_row(available_concepts, pic, mask)
            label_as_nr = int(label_encoder.transform([label])[0])
            y.append(label_as_nr)
            X.append(row)

        valid_X, valid_y = [], []
        for x_i, y_i in zip(X, y):
            y_as_label = label_encoder.inverse_transform([y_i])[0]
            if y_as_label in valid_labels:
                valid_X.append(x_i)
                valid_y.append(y_i)

        for i, y_i in enumerate(valid_y):
            y_as_label = label_encoder.inverse_transform([y_i])[0]
            if y_as_label == counter_factual_class:
                valid_y[i] = COUNTERFACTUAL_LABEL
            else:
                valid_y[i] = ORIGINAL
        for i, y_i in enumerate(y):
            y_as_label = label_encoder.inverse_transform([y_i])[0]
            if y_as_label == counter_factual_class:
                y[i] = COUNTERFACTUAL_LABEL
            else:
                y[i] = ORIGINAL

        clf = train_decision_tree(valid_X, valid_y)
        return X, y, clf

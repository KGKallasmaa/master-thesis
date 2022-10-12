from typing import List

import dice_ml
import pandas as pd
from pymongo import MongoClient
from main.database.explanation_requirement import ExplanationRequirementDb
from main.models.explanation_requirement import ExplanationRequirement
from main.service.explain.explain import encode_categorical_values, get_training_row, train_decision_tree
from main.service.pre_explanation.data_access import get_labels, get_images, get_masks
import numpy as np


class CounterFactualExplanationService:
    explanation_requirement_db: ExplanationRequirementDb

    def __init__(self, client: MongoClient):
        self.explanation_requirement_db = ExplanationRequirementDb(client)

    def counterfactual_explanation(self,
                                   explanation_id: str,
                                   to_be_explained_image_index: int,
                                   counter_factual_class: str):
        explanation_requirement = self.explanation_requirement_db.get_explanation_requirement(explanation_id)

        label_encoder, X, y, decision_tree = self.__regular_explain_tree(explanation_requirement)
        decision_tree.fit(X, y)

        # 1. Initialize dice
        dice_explanation = dice_ml.Model(model=decision_tree, backend="sklearn")
        dice_transformed_data = self.__transform_data_for_dice(
            X, y,
            explanation_requirement.available_concepts,
            label_encoder
        )

        dice_data = dice_ml.Data(dataframe=dice_transformed_data,
                                 continuous_features=explanation_requirement.available_concepts,
                                 outcome_name="label")

        # 2. Initialize the explainer
        exp = dice_ml.Dice(dice_data, dice_explanation, method="random")

        # 3. Generate the counterfactual
        # to_be_explained_instance = dice_transformed_data.iloc[to_be_explained_image_index].to_dict()
        to_be_explained_instance = dice_transformed_data.to_dict(orient='records')[to_be_explained_image_index]

        original_class = to_be_explained_instance["label"]
        del to_be_explained_instance["label"]
        to_be_explained_instance = pd.DataFrame(to_be_explained_instance, index=[0])

        try:
            counterfactual = exp.generate_counterfactuals(query_instances=to_be_explained_instance,
                                                          total_CFs=1,
                                                          desired_class=counter_factual_class)
            return {
                "originalClass": original_class,
                "counterFactualExplanation": counterfactual.visualize_as_list(),
            }
        except Exception as e:
            print(e, flush=True)
            return {
                "originalClass": "",
                "counterFactualExplanation": [],
                "error": "Could not generate counterfactuals. %s" % e
            }

    @staticmethod
    def __transform_data_for_dice(X, y, concepts: List[str], label_encoder):
        data = {}
        for x_i, y_i in zip(X, y):
            current_y_values = data.get("label", [])
            current_y_values.append(label_encoder.inverse_transform([y_i])[0])
            data["label"] = current_y_values

            for i, c in enumerate(concepts):
                current_c_values = data.get(c, [])
                current_c_values.append(x_i[i])
                data[c] = current_c_values
        return pd.DataFrame(data=data)

    @staticmethod
    def __regular_explain_tree(explanation_requirement: ExplanationRequirement):
        available_concepts = explanation_requirement.available_concepts
        available_concepts.sort()

        if len(available_concepts) == 0:
            raise RuntimeError("Explanation can not be provided, because we can not use any concepts")

        label_encoder = encode_categorical_values(get_labels())
        X, y = [], []
        for label, pic, mask in zip(get_labels(), get_images(), get_masks()):
            row = get_training_row(available_concepts, pic, mask)
            label_as_nr = label_encoder.transform([label])[0]
            y.append(label_as_nr)
            X.append(row)

        clf = train_decision_tree(np.array(X), np.array(y))
        return label_encoder, X, y, clf

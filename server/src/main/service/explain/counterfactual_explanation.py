import math
from typing import List

from pymongo import MongoClient
from main.database.explanation_requirement import ExplanationRequirementDb
from main.service.explain.explain import encode_categorical_values, get_training_row, train_decision_tree
from main.service.explain.human_readable_explanation import HumanReadableExplanationService
from main.service.pre_explanation.data_access import get_labels, get_images, get_masks
import numpy as np


class CounterFactualExplanationService:
    explanation_requirement_db: ExplanationRequirementDb

    def __init__(self, client: MongoClient):
        self.explanation_requirement_db = ExplanationRequirementDb(client)

    def counterfactual_explanation(self, explanation_id: str):
        constrains = self.explanation_requirement_db.get_explanation_requirement(explanation_id)
        available_concepts = constrains.available_concepts

        label_encoder, testing_data, testing_labels, decision_tree = self.__regular_explain_tree(explanation_id)
        feature_encoder = encode_categorical_values(available_concepts)

        print("HELLLLLO", flush=True)

        excluded_node_ids = self.__mark_non_counterfactuals_as_none(
            constrains.counter_factual,
            decision_tree,
            label_encoder,
            testing_data
        )
        print("excluded node ids", flush=True)
        print(excluded_node_ids, flush=True)

        hre = HumanReadableExplanationService(label_encoder=label_encoder,
                                              feature_encoder=feature_encoder,
                                              estimator=decision_tree)

        return hre.human_readable_counterfactual_explanation(y_true=testing_labels,
                                                             counterfacutal_label=constrains.counter_factual,
                                                             excluded_nodes=excluded_node_ids)

    def __regular_explain_tree(self, explanation_id):
        constrains = self.explanation_requirement_db.get_explanation_requirement(explanation_id)
        available_concepts = constrains.available_concepts
        available_concepts.sort()

        if len(available_concepts) == 0:
            raise RuntimeError("Explanation can not be provided, because we can not use any concepts")

        label_encoder = encode_categorical_values(get_labels())
        training_data, training_labels, testing_data, testing_labels = [], [], [], []

        for index, (label, pic, mask) in enumerate(zip(get_labels(), get_images(), get_masks())):
            row = get_training_row(available_concepts, pic, mask)
            label_as_nr = label_encoder.transform([label])

            if index == constrains.original_image_id:
                testing_labels.append(label_as_nr)
                testing_data.append(row)
            else:
                training_labels.append(label_as_nr)
                training_data.append(row)

        clf = train_decision_tree(np.array(training_data), np.array(training_labels))
        return label_encoder, testing_data, testing_labels, clf

    @staticmethod
    def __mark_non_counterfactuals_as_none(counter_factual_class: str, decision_tree, label_encoder, x_test) -> List[
        int]:
        decision_paths = decision_tree.decision_path(x_test).toarray()
        leave_id = decision_tree.apply(x_test)

        all_node_indexes = [*range(0, len(decision_paths[0]))]

        to_be_excluded_nodes = []
        for i, decision_path in enumerate(decision_paths):
            for node_index, node_value in enumerate(decision_path):
                if node_index in to_be_excluded_nodes:
                    continue
                is_leaf_node = leave_id[i] == node_index
                if not is_leaf_node:
                    continue
                leaf_category = label_encoder.inverse_transform([node_index])[0]
                is_counterfactual_class = leaf_category == counter_factual_class
                if is_counterfactual_class:
                    all_node_indexes[node_index] = None
                    to_be_excluded_nodes.append(node_index)

        return to_be_excluded_nodes

    @staticmethod
    def find_all_parents(node_id: int) -> List[int]:
        if node_id <= 0:
            return []
        all_parents = []
        current_node = node_id
        while 1:
            node_parent = math.floor((current_node - 1) / 2)
            if node_parent <= 0:
                return all_parents
            all_parents.append(node_parent)
            current_node = node_parent

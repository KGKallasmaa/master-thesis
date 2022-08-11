import math
from typing import List, Optional

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

        label_encoder, training_data, training_labels, testing_data, testing_labels, decision_tree = self.__regular_explain_tree(
            explanation_id)
        feature_encoder = encode_categorical_values(available_concepts)

        predictions = decision_tree.predict(testing_data)

        excluded_node_ids = self.find_excluded_node_ids(
            constrains.counter_factual,
            decision_tree,
            label_encoder,
            testing_data,
            testing_labels
        )
        print(excluded_node_ids, flush=True)

        hre = HumanReadableExplanationService(label_encoder=label_encoder,
                                              feature_encoder=feature_encoder,
                                              estimator=decision_tree)
        return hre.human_readable_explanation(x_test=testing_data,
                                              y_test=predictions,
                                              y_true=testing_labels,
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
        return label_encoder, training_data, training_labels, testing_data, testing_labels, clf

    def find_excluded_node_ids(self, counter_factual_class: str, decision_tree, label_encoder, x_test, y_test) -> List[
        int]:
        "Excluding all nodes that don't lead to the counterfactual class"
        all_nodes = self.__mark_non_counterfactuals_as_none(counter_factual_class, decision_tree, label_encoder, x_test,
                                                            y_test)

        to_be_excluded_nodes = [i for i, node_val in enumerate(all_nodes) if node_val is None]
        to_be_excluded_nodes.sort()
        return to_be_excluded_nodes

    def __mark_non_counterfactuals_as_none(self, counter_factual_class: str, decision_tree, label_encoder, x_test,
                                           y_test):
        node_indicator = decision_tree.decision_path(x_test)
        leave_id = decision_tree.apply(x_test)

        sample_id = 0
        node_index = node_indicator.indices[node_indicator.indptr[sample_id]:
                                            node_indicator.indptr[sample_id + 1]]

        all_nodes = [node_indicator.indptr[node_id] for node_id in node_index]
        for node_index in range(1, len(node_index), 1):
            is_leaf_node = leave_id[sample_id] == node_index
            if not is_leaf_node:
                continue
            leaf_category = label_encoder.inverse_transform([y_test])[0]
            is_not_counterfactual_class = leaf_category != counter_factual_class
            if not is_not_counterfactual_class:
                continue
            all_nodes[node_index] = None
        for i in range(len(all_nodes)):
            should_be_none = self.__should_be_null(all_nodes, i)
            if should_be_none:
                all_nodes[i] = None
        return all_nodes

    def __should_be_null(self, all_nodes: List[str], my_index: int) -> bool:
        if my_index <= 0:
            return False
        if my_index > len(all_nodes):
            return False
        parent = self.__parent(my_index, all_nodes)
        if parent is None:
            return True
        left_child = self.__left_child(my_index, all_nodes)
        right_child = self.__right_child(my_index, all_nodes)
        if left_child and right_child:
            return False
        if left_child is None and right_child is None:
            return True
        left_child_id = int(2 * my_index + 1)
        right_child_id = int(2 * my_index + 2)
        return self.__should_be_null(all_nodes, left_child_id) and self.__should_be_null(all_nodes, right_child_id)

    @staticmethod
    def __parent(my_id: int, all_nodes: List[str]) -> Optional[str]:
        try:
            return all_nodes[math.floor((my_id - 1) / 2)]
        except Exception as e:
            return None

    @staticmethod
    def __left_child(my_id: int, all_nodes: List[str]) -> Optional[str]:
        try:
            return all_nodes[int(2 * my_id + 1)]
        except Exception as e:
            return None

    @staticmethod
    def __right_child(my_id: int, all_nodes: List[str]) -> Optional[str]:
        try:
            return all_nodes[int(2 * my_id + 2)]
        except Exception as e:
            return None

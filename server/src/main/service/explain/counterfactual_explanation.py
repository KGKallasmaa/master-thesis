import math
from typing import List

from alibi.explainers import Counterfactual
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
        excluded_node_ids = self.__to_be_excluded_node_ids(explanation_id, constrains.counter_factual)
        feature_encoder = encode_categorical_values(constrains.available_concepts)
        label_encoder, X, y, decision_tree = self.__regular_explain_tree(explanation_id)
        """
        available_concepts = constrains.available_concepts
        label_encoder, X, y, decision_tree = self.__regular_explain_tree(explanation_id)
        feature_encoder = encode_categorical_values(available_concepts)
        excluded_node_ids = self.__to_be_excluded_node_ids(explanation_id, constrains.counter_factual)
        """
        print(X,flush=True)
        shape = (1,len(X[0]))
        cf = Counterfactual(decision_tree, shape, distance_fn='l1', target_proba=1.0,
                            target_class=constrains.counter_factual, max_iter=1000, early_stop=50, lam_init=1e-1,
                            max_lam_steps=10, tol=0.05, learning_rate_init=0.1,
                            feature_range=(-1e10, 1e10), eps=0.01, init='identity',
                            decay=True, write_dir=None, debug=True)
        explanation = cf.explain(X)

        print("FINALLY WE ARE HERE!!!!!!")
        print(explanation,flush=True)
        return explanation

        """
        hre = HumanReadableExplanationService(label_encoder=label_encoder,
                                              feature_encoder=feature_encoder,
                                              estimator=decision_tree)

        return hre.human_readable_counterfactual_explanation(counterfacutal_label=constrains.counter_factual,
                                                             excluded_nodes=excluded_node_ids)
        """

    def __to_be_excluded_node_ids(self, explanation_id: str, counterfactual_class: str) -> List[int]:
        """
        We are excluding some nodes, cause they lead to our target class
        """
        label_encoder, X, y, decision_tree = self.__regular_explain_tree(explanation_id)
        return self.__nodes_leading_to_counterfactual(
            counterfactual_class,
            decision_tree,
            label_encoder,
            X)

    def __regular_explain_tree(self, explanation_id:str):
        constrains = self.explanation_requirement_db.get_explanation_requirement(explanation_id)
        available_concepts = constrains.available_concepts
        available_concepts.sort()

        if len(available_concepts) == 0:
            raise RuntimeError("Explanation can not be provided, because we can not use any concepts")

        label_encoder = encode_categorical_values(get_labels())
        training_data, training_labels = [], []
        for index, (label, pic, mask) in enumerate(zip(get_labels(), get_images(), get_masks())):
            row = get_training_row(available_concepts, pic, mask)
            label_as_nr = label_encoder.transform([label])
            training_labels.append(label_as_nr)
            training_data.append(row)

        clf = train_decision_tree(np.array(training_data), np.array(training_labels))
        return label_encoder, training_data, training_labels, clf


    @staticmethod
    def __nodes_leading_to_counterfactual(counter_factual_class: str, decision_tree, label_encoder, features) -> List[
        int]:
        decision_paths = decision_tree.decision_path(features).toarray()
        leaf_ids = decision_tree.apply(features)
        print("unique leaf ids: " + str(list(set(leaf_ids))), flush=True)

        nodes_leading_to_target_class = []
        for i, decision_path in enumerate(decision_paths):
            leaf_category = label_encoder.inverse_transform([leaf_ids[i]])[0]
            is_counterfactual_class = leaf_category == counter_factual_class
            if is_counterfactual_class:
                nodes_leading_to_target_class += [i for i, node_value in enumerate(decision_path) if node_value == 1]

        nodes_leading_to_target_class = list(set(nodes_leading_to_target_class))
        print("nodes leading to target class" + str(list(nodes_leading_to_target_class)), flush=True)
        return sorted(nodes_leading_to_target_class)

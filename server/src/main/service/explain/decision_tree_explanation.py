from typing import List, Dict, Generator

import numpy as np

from main.database.closest_labels import ClosestLabelsDb
from main.database.explanation_requirement import ExplanationRequirementDb
from main.service.explain.common import encode_categorical_values, get_training_row, train_decision_tree
from main.service.explain.human_readable_explanation import HumanReadableExplanationService
from main.service.pre_explanation.data_access import get_labels, get_images, get_masks

class DecisionTreeExplanationService:
    def __init__(self):
        self.requirement_db = ExplanationRequirementDb()
        self.closest_label_db = ClosestLabelsDb()
        self.best_accuracy = 0
        self.explanations = {}

    def explain(self, explanation_id: str, to_be_explained_image_index: int) -> Dict[str, any]:
        for concepts in self.to_be_used_concepts(explanation_id):
            concepts.sort()
            self.explain_using_decision_tree(to_be_explained_image_index, concepts)
        return self.explanations

    def explain_using_decision_tree(self, to_be_explained_image_index: int, decision_tree_concepts: List[str]) -> None:
        closest = self.closest_label_db.get_by_image_id(to_be_explained_image_index)
        valid_labels = [closest.label] + closest.closest

        label_encoder = encode_categorical_values(get_labels())
        feature_encoder = encode_categorical_values(decision_tree_concepts)

        training_data, training_labels, testing_data, testing_labels = [], [], [], []

        # TDO: we should not loop over every single image
        for index, (label, pic, mask) in enumerate(zip(get_labels(), get_images(), get_masks())):
            if label not in valid_labels:
                continue
            row = get_training_row(decision_tree_concepts, pic, mask)
            label_as_nr = label_encoder.transform([label])

            if index == to_be_explained_image_index:
                testing_labels.append(label_as_nr)
                testing_data.append(row)
            else:
                training_labels.append(label_as_nr)
                training_data.append(row)

        clf, accuracy = train_decision_tree(np.array(training_data), np.array(training_labels))

        if accuracy <= self.best_accuracy:
            return None

        self.best_accuracy = accuracy

        predictions = clf.predict(testing_data)
        hre = HumanReadableExplanationService(label_encoder=label_encoder,
                                              feature_encoder=feature_encoder,
                                              estimator=clf)
        self.explanations = hre.human_readable_explanation(x_test=testing_data, y_test=predictions,
                                                           y_true=testing_labels)

    def to_be_used_concepts(self, explanation_id: str) -> Generator[List[str], None, None]:
        constraints = self.requirement_db.get_explanation_requirement(explanation_id).constraints

        print(explanation_id, flush=True)
        print(constraints.to_db_value(), flush=True)

        must_have_concepts = constraints.user_selected_concepts
        if len(must_have_concepts) == 0:
            must_have_concepts = constraints.initially_proposed_concepts

        if len(must_have_concepts) == 0:
            raise ValueError("Decision tree explanation requires at least one concept for explanation")

        yield must_have_concepts

        last_entry = must_have_concepts.copy()
        for c in constraints.all_unique_constraints():
            if c not in last_entry:
                last_entry.append(c)
                yield last_entry

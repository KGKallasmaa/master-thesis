from typing import List, Dict

import numpy as np

from main.database.closest_labels import ClosestLabelsDb
from main.database.explanation_requirement import ExplanationRequirementDb
from main.service.explain.common import encode_categorical_values, get_training_row, train_decision_tree
from main.service.explain.human_readable_explanation import HumanReadableExplanationService
from main.service.pre_explanation.data_access import get_labels, get_images, get_masks

DECISION_TREE = "decision_tree"
COUNTERFACTUAL = "counterfactual"


class DecisionTreeExplanationService:
    def __init__(self):
        self.requirement_db = ExplanationRequirementDb()
        self.closest_label_db = ClosestLabelsDb()

    def explain(self, explanation_id: str, to_be_explained_image_index: int) -> Dict[str, any]:
        concepts = self.to_be_used_concepts(explanation_id)
        self.update_used_constraints(explanation_id, concepts)
        return self.explain_using_decision_tree(explanation_id, to_be_explained_image_index, concepts)

    def explain_using_decision_tree(self, explanation_id: str, to_be_explained_image_index: int,
                                    decision_tree_concepts: List[str])-> Dict[str, any]:
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


        predictions = clf.predict(testing_data)
        hre = HumanReadableExplanationService(label_encoder=label_encoder,
                                              feature_encoder=feature_encoder,
                                              estimator=clf)
        return hre.human_readable_explanation(x_test=testing_data, y_test=predictions,y_true=testing_labels)

    # TODO: fix this
    def to_be_used_concepts(self, explanation_id: str) -> List[str]:
        constraints = self.requirement_db.get_explanation_requirement(explanation_id).constraints
        human_readable_concepts = constraints.user_selected_concepts
        if len(human_readable_concepts) == 0:
            human_readable_concepts = constraints.initially_proposed_concepts
        if len(human_readable_concepts) == 0:
            raise ValueError("Decision tree explanation requires at least one concept for explanation")
        return human_readable_concepts

    def update_used_constraints(self, explanation_id: str, used: List[str]):
        requirement = self.requirement_db.get_explanation_requirement(explanation_id)
        requirement.constraints.change_currently_used_concepts(DECISION_TREE, used)
        self.requirement_db.update_explanation_requirement_constraints(requirement)

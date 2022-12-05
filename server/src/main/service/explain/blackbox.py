from typing import List

from main.database.constraint_db import ConstraintDb
from main.database.explanation_requirement import ExplanationRequirementDb
from main.models.desision_tree_explanation_response import DecisionTreeExplanationResponse
from main.service.explain.decision_tree_explanation import explain_using_decision_tree
from main.service.pre_explanation.data_access import get_labels
import numpy as np

RANDOM_N_LABELS = 10
all_labels = get_labels()
valid_blackbox_labels = all_labels[np.random.choice(len(all_labels), size=RANDOM_N_LABELS, replace=False)]


class BlackBoxModelService:
    def __init__(self):
        self.explanation_requirement_db = ExplanationRequirementDb()
        self.constraint_db = ConstraintDb()

    def execute(self, explanation_id: str, initial_concepts: List[str]) -> float:
        explanation_requirement = self.explanation_requirement_db.get_explanation_requirement(explanation_id)

        return explain_using_decision_tree(
            valid_labels=get_labels(),
            to_be_explained_image_index=explanation_requirement.original_image_id,
            decision_tree_concepts=initial_concepts).accuracy

    # TODO: use it in counterfactual explanations
    def black_box_model(self, explanation_id: str) -> DecisionTreeExplanationResponse:
        explanation_requirement = self.explanation_requirement_db.get_explanation_requirement(explanation_id)
        constraints = self.constraint_db.get_constraint_by_explanation_requirement_id(explanation_id)

        return explain_using_decision_tree(
            valid_labels=valid_blackbox_labels,
            to_be_explained_image_index=explanation_requirement.original_image_id,
            decision_tree_concepts=constraints.initially_proposed_concepts)

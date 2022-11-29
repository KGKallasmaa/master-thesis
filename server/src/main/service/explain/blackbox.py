from typing import List

from main.database.constraint_db import ConstraintDb
from main.database.explanation_requirement import ExplanationRequirementDb
from main.models.enums import ExplanationType
from main.service.explain.decision_tree_explanation import DecisionTreeExplanationService
from main.service.perfromance.performance_service import PerformanceService


class BlackBoxModelService:
    def __init__(self):
        self.performance_service = PerformanceService()
        self.decision_tree_explainer = DecisionTreeExplanationService()
        self.explanation_requirement_db = ExplanationRequirementDb()
        self.constraint_db = ConstraintDb()

    def execute(self, explanation_id: str, initial_concepts: List[str]):
        explanation_requirement = self.explanation_requirement_db.get_explanation_requirement(explanation_id)

        feature_encoder, estimator, accuracy, explanation = self.decision_tree_explainer.explain_using_decision_tree(
            to_be_explained_image_index=explanation_requirement.original_image_id,
            decision_tree_concepts=initial_concepts)

        self.performance_service.update_accuracy(accuracy, ExplanationType.BLACK_BOX, explanation_id)

    def black_box_model(self, explanation_id: str):
        # TODO: use it in counterfactual explanations
        explanation_requirement = self.explanation_requirement_db.get_explanation_requirement(explanation_id)
        constraints = self.constraint_db.get_constraint_by_explanation_requirement_id(explanation_id)

        _, estimator, accuracy, explanation = self.decision_tree_explainer.explain_using_decision_tree(
            to_be_explained_image_index=explanation_requirement.original_image_id,
            decision_tree_concepts=constraints.initially_proposed_concepts)
        return estimator

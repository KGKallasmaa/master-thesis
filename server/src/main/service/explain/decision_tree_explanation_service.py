from typing import List, Dict


from main.database.closest_labels import ClosestLabelsDb
from main.database.constraint_db import ConstraintDb
from main.database.explanation_requirement import ExplanationRequirementDb
from main.models.desision_tree_explanation_response import DecisionTreeExplanationResponse
from main.models.enums import ExplanationType
from main.service.explain.decision_tree_explanation import explain_using_decision_tree
from main.service.perfromance.performance_service import PerformanceService


class DecisionTreeExplanationService:
    def __init__(self):
        self.requirement_db = ExplanationRequirementDb()
        self.closest_label_db = ClosestLabelsDb()
        self.constraint_db = ConstraintDb()
        self.performance_service = PerformanceService()

    def explain(self, explanation_id: str, to_be_explained_image_index: int) -> Dict[str, any]:
        concepts = self.to_be_used_concepts(explanation_id)
        response = self.__explain_using_decision_tree(
            to_be_explained_image_index,
            concepts)
        self.update_used_constraints(explanation_id=explanation_id,
                                        feature_encoder=response.feature_encoder,
                                     estimator=response.model)

        self.performance_service.update_decision_tree_performance(response, explanation_id)
        return response.explanation

    def __explain_using_decision_tree(self, to_be_explained_image_index: int,decision_tree_concepts: List[str]) -> DecisionTreeExplanationResponse:
        closest = self.closest_label_db.get_by_image_id(to_be_explained_image_index)
        valid_labels = [closest.label] + closest.closest
        return explain_using_decision_tree(valid_labels, to_be_explained_image_index, decision_tree_concepts)

    def to_be_used_concepts(self, explanation_id: str) -> List[str]:
        constraints = self.constraint_db.get_constraint_by_explanation_requirement_id(explanation_id)
        human_readable_concepts = constraints.user_selected_concepts[ExplanationType.DECISION_TREE.value]
        if len(human_readable_concepts) == 0:
            human_readable_concepts = constraints.initially_proposed_concepts
        if len(human_readable_concepts) == 0:
            raise ValueError("Decision tree explanation requires at least one concept for explanation")
        return human_readable_concepts

    def update_used_constraints(self, explanation_id: str, feature_encoder, estimator):
        feature_importance = {feature: {"featureName": feature, "local": importance} for feature, importance in
                              zip(feature_encoder.classes_, estimator.feature_importances_)}

        feature_importance = sorted(list(feature_importance.values()), key=lambda x: x["local"], reverse=True)
        most_predictive_features = [feature["featureName"] for feature in feature_importance]

        constraints = self.constraint_db.get_constraint_by_explanation_requirement_id(explanation_id)

        constraints.change_concept_constraint("most_predictive_concepts", ExplanationType.DECISION_TREE,
                                              most_predictive_features)

        self.constraint_db.update_constraint(constraints)

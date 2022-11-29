from main.database.performance_db import PerformanceDb
from main.models.enums import ExplanationType
from main.service.pre_explanation.data_access import get_labels


class PerformanceService:
    def __init__(self):
        self.performance_repository = PerformanceDb()
        self.labels = get_labels()

    def update_accuracy(self,
                        accuracy: float,
                        explanation_type: ExplanationType,
                        explanation_requirement_id: str):
        performance = self.performance_repository.get_by_explanation_requirement_id(explanation_requirement_id)
        match explanation_type:
            case ExplanationType.DECISION_TREE:
                performance.update_decision_tree(accuracy)
            case ExplanationType.BLACK_BOX:
                performance.update_blackbox(accuracy)
        self.performance_repository.update(performance)

    def update_counterfactual_probability(self, probability: float, explanation_requirement_id: str):
        performance = self.performance_repository.get_by_explanation_requirement_id(explanation_requirement_id)
        performance.update_counterfactual(probability)
        self.performance_repository.update(performance)

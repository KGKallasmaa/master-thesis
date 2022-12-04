from sklearn.metrics import accuracy_score

from main.database.explanation_requirement import ExplanationRequirementDb
from main.database.performance_db import PerformanceDb
from main.models.desision_tree_explanation_response import DecisionTreeExplanationResponse
from main.service.explain.blackbox import BlackBoxModelService
from main.service.pre_explanation.data_access import get_labels


class PerformanceService:
    def __init__(self):
        self.performance_repository = PerformanceDb()
        self.explanation_requirement_db = ExplanationRequirementDb()
        self.black_box_explainer = BlackBoxModelService()
        self.labels = get_labels()

    def update_blackbox_accuracy(self,
                                 accuracy: float,
                                 explanation_requirement_id: str):
        performance = self.performance_repository.get_by_explanation_requirement_id(explanation_requirement_id)
        performance.update_blackbox(accuracy)
        self.performance_repository.update(performance)

    def update_decision_tree_performance(self,
                                         decision_tree: DecisionTreeExplanationResponse,
                                         explanation_requirement_id: str):
        performance = self.performance_repository.get_by_explanation_requirement_id(explanation_requirement_id)

        black_box = self.black_box_explainer.black_box_model(explanation_requirement_id)

        labels = get_labels()
        blackbox_predictions_for_allowed_labels = [prediction for i, prediction in enumerate(black_box.transformed_all_predictions)
                                                   if labels[i] in decision_tree.allowed_labels]

        assert len(blackbox_predictions_for_allowed_labels) == len(decision_tree.transformed_predictions)

        fidelity = accuracy_score(blackbox_predictions_for_allowed_labels, decision_tree.transformed_predictions)
        accuracy = decision_tree.accuracy

        print("desision_tree-predictions", flush=True)
        print(decision_tree.transformed_predictions, flush=True)
        print("black-box-predictions", flush=True)
        print(black_box.transformed_predictions, flush=True)
        print("true labels")
        print(decision_tree.transformed_y_test, flush=True)
        print("desision-tree-accuracy", flush=True)
        print(accuracy)
        print("desision-tree-fidelity", flush=True)
        print(fidelity)

        performance.update_decision_tree(decision_tree.accuracy, fidelity)
        self.performance_repository.update(performance)

    def update_counterfactual_probability(self, probability: float, explanation_requirement_id: str):
        performance = self.performance_repository.get_by_explanation_requirement_id(explanation_requirement_id)
        performance.update_counterfactual(probability)
        self.performance_repository.update(performance)

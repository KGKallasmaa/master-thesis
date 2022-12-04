from sklearn.metrics import accuracy_score

from main.database.performance_db import PerformanceDb
from main.models.desision_tree_explanation_response import DecisionTreeExplanationResponse
from main.service.explain.blackbox import BlackBoxModelService
from main.service.pre_explanation.data_access import get_labels


class PerformanceService:
    def __init__(self):
        self.performance_repository = PerformanceDb()
        self.black_box_explainer = BlackBoxModelService()
        self.labels = get_labels()

    def update_blackbox_accuracy(self,
                                 accuracy: float,
                                 explanation_requirement_id: str):
        performance = self.performance_repository.get_by_explanation_requirement_id(explanation_requirement_id)
        performance.update_blackbox(accuracy)
        self.performance_repository.update(performance)

    def update_decision_tree_accuracy(self,
                                      response: DecisionTreeExplanationResponse,
                                      explanation_requirement_id: str):
        performance = self.performance_repository.get_by_explanation_requirement_id(explanation_requirement_id)

        black_box = self.black_box_explainer.black_box_model(explanation_requirement_id)

        fidelity = accuracy_score(black_box.transformed_predictions, response.transformed_predictions)
        accuracy = response.accuracy

        print("desision_tree-predictions", flush=True)
        print(response.transformed_predictions, flush=True)
        print("black-box-predictions", flush=True)
        print(black_box.transformed_predictions, flush=True)
        print("true labels")
        print(response.transformed_y_test, flush=True)
        print("desision-tree-accuracy", flush=True)
        print(accuracy)
        print("desision-tree-fidelity", flush=True)
        print(fidelity)

        performance.update_decision_tree(accuracy, fidelity)
        self.performance_repository.update(performance)

    def update_counterfactual_probability(self, probability: float, explanation_requirement_id: str):
        performance = self.performance_repository.get_by_explanation_requirement_id(explanation_requirement_id)
        performance.update_counterfactual(probability)
        self.performance_repository.update(performance)

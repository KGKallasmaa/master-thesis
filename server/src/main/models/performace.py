from typing import Dict


class Performance:
    def __init__(self, json: Dict[str, any]):
        self.explanation_requirement_id = json["explanationRequirementId"]
        self.blackbox = json.get("blackbox", {
            "accuracy": None,
        })
        self.decision_tree = json.get("decisionTree", {
            # how accurately it predicts the true labels
            "accuracy": None,
            # how accurately it mimics the blackbox
            "fidelity": None,
        })
        self.counterfactual = json.get("counterfactual", {
            "probability": None,
        })

    def to_db_value(self) -> Dict[str, any]:
        return {
            'explanationRequirementId': self.explanation_requirement_id,
            'blackbox': self.blackbox,
            'decisionTree': self.decision_tree,
            'counterfactual': self.counterfactual,
        }

    def update_decision_tree(self, accuracy: float, fidelity: float):
        if accuracy > 1.0 or accuracy < 0.0:
            raise ValueError(f"Accuracy must be between 0 and 1, got {accuracy}")
        if fidelity > 1.0 or fidelity < 0.0:
            raise ValueError(f"Fidelity must be between 0 and 1, got {fidelity}")
        self.decision_tree["accuracy"] = accuracy
        self.decision_tree["fidelity"] = fidelity

    def update_blackbox(self, accuracy: float):
        if accuracy > 1.0 or accuracy < 0.0:
            raise ValueError(f"Accuracy must be between 0 and 1, got {accuracy}")
        self.blackbox["accuracy"] = accuracy

    def update_counterfactual(self, probability: float):
        if probability > 1.0 or probability < 0.0:
            raise ValueError(f"Probability must be between 0 and 1, got {probability}")
        self.counterfactual["probability"] = probability

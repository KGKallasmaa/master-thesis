from enum import Enum


class ExplanationType(Enum):
    DECISION_TREE = "decision_tree"
    COUNTERFACTUAL = "counterfactual"

    @staticmethod
    def from_str(label):
        if label == "decision_tree":
            return ExplanationType.DECISION_TREE
        elif label == "counterfactual":
            return ExplanationType.COUNTERFACTUAL
        raise ValueError(f"Invalid explanation type: {label}")

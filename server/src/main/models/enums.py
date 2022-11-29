from enum import Enum


class ExplanationType(str, Enum):
    DECISION_TREE = "decision_tree"
    COUNTERFACTUAL = "counterfactual"
    BLACK_BOX = "black_box"

    @staticmethod
    def from_str(label):
        if label == "decision_tree":
            return ExplanationType.DECISION_TREE
        elif label == "counterfactual":
            return ExplanationType.COUNTERFACTUAL
        elif label == "black_box":
            return ExplanationType.BLACK_BOX
        raise ValueError(f"Invalid explanation type: {label}")

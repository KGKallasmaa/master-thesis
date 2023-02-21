from enum import Enum


class ExplanationType(str, Enum):
    DECISION_TREE = "decision_tree"
    COUNTERFACTUAL = "counterfactual"
    BLACK_BOX = "black_box"

    @staticmethod
    def from_str(label):
        match label:
            case "decision_tree":
                return ExplanationType.DECISION_TREE
            case "counterfactual":
                return ExplanationType.COUNTERFACTUAL
            case "black_box":
                return ExplanationType.BLACK_BOX
            case _:
                raise ValueError(f"Invalid explanation type: {label}")

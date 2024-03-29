from typing import Dict

from main.models.enums import ExplanationType


class Constraints:
    def __init__(self, json: Dict[str, any]):
        self.explanation_requirement_id = json["explanation_requirement_id"]
        self.initially_proposed_concepts = json.get("initially_proposed_concepts", [])

        self.most_predictive_concepts = json.get("most_predictive_concepts", {
            ExplanationType.DECISION_TREE.value: [],
            ExplanationType.COUNTERFACTUAL.value: [],
        })

        self.user_selected_concepts = json.get("user_selected_concepts", {
            ExplanationType.DECISION_TREE.value: [],
            ExplanationType.COUNTERFACTUAL.value: [],
        })

    def change_concept_constraint(self,
                                  constraint_type: str,
                                  explanation_type: ExplanationType,
                                  new_values: list[str]):

        match constraint_type:
            case "initially_proposed_concepts":
                self.initially_proposed_concepts = new_values
                self.user_selected_concepts[ExplanationType.DECISION_TREE.value] = new_values
                self.user_selected_concepts[ExplanationType.COUNTERFACTUAL.value] = new_values
            case "most_predictive_concepts":
                self.most_predictive_concepts[explanation_type.value] = new_values
            case "user_selected_concepts":
                self.user_selected_concepts[explanation_type.value] = new_values
            case _:
                raise ValueError(f"Unknown constraint type: {constraint_type}")

    def to_db_value(self) -> Dict[str, any]:
        return {
            'explanation_requirement_id': self.explanation_requirement_id,
            'initially_proposed_concepts': self.initially_proposed_concepts,
            'most_predictive_concepts': self.most_predictive_concepts,
            'user_selected_concepts': self.user_selected_concepts,
        }

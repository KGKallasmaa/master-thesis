from typing import Dict


class Constraints:
    def __init__(self, json: Dict[str, any]):
        self.explanation_requirement_id = json["explanation_requirement_id"]
        self.initially_proposed_concepts = json.get("initially_proposed_concepts", [])


        self.most_predictive_concepts = json.get("most_predictive_concepts", {
            "decision_tree": [],
            "counterfactual": [],
        })

        self.user_selected_concepts = json.get("user_selected_concepts", {
            "decision_tree": [],
            "counterfactual": [],
        })

    def change_concept_constraint(self,
                                  constraint_type: str,
                                    explanation_type: str,
                                  new_values: list[str]):

        if constraint_type == "initially_proposed_concepts":
            self.initially_proposed_concepts = new_values
            return
        if explanation_type not in {"decision_tree", "counterfactual"}:
            raise ValueError(f"Unknown explanation type: {explanation_type}")

        if constraint_type == "most_predictive_concepts":
            self.most_predictive_concepts[explanation_type] = new_values
        elif constraint_type == "user_selected_concepts":
            self.user_selected_concepts[explanation_type] = new_values
        else:
            raise ValueError(f"Unknown constraint type: {constraint_type}")


    def to_db_value(self) -> Dict[str, any]:
        return {
            'initially_proposed_concepts': self.initially_proposed_concepts,
            'most_predictive_concepts': self.most_predictive_concepts,
            'user_selected_concepts': self.user_selected_concepts,
        }

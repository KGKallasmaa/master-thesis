from typing import Dict


class Constraints:
    def __init__(self, json: Dict[str, any]):
        self.initially_proposed_concepts = json.get("initially_proposed_concepts", [])
        self.most_predictive_concepts = json.get("most_predictive_concepts", [])
        self.most_intuitive_concepts = json.get("most_intuitive_concepts", [])
        self.currently_used_concepts = json.get("currently_used_concepts", {
            "decision_tree": [],
            "counterfactual": [],
        })
        self.user_selected_concepts = json.get("user_selected_concepts", [])


    def change_concept_constraint(self,
                                  constraint_type: str,
                                  new_values: list[str]):

        if constraint_type == "currently_used_concepts":
            self.currently_used_concepts = new_values
        elif constraint_type == "initially_proposed_concepts":
            self.initially_proposed_concepts = new_values
        elif constraint_type == "most_intuitive_concepts":
            self.most_intuitive_concepts = new_values
        elif constraint_type == "most_predictive_concepts":
            self.most_predictive_concepts = new_values
        elif constraint_type == "user_selected_concepts":
            self.user_selected_concepts = new_values
        else:
            raise ValueError(f"Unknown constraint type: {constraint_type}")

    def available_to_be_chosen_concepts(self, explanation_type: str):
        if explanation_type not in {"decision_tree", "counterfactual"}:
            raise ValueError(f"Unknown explanation type: {explanation_type}")

        new_concepts = self.user_selected_concepts
        for predictive_concept, intuitive_concept in zip(self.most_predictive_concepts, self.most_intuitive_concepts):
            if predictive_concept not in new_concepts:
                new_concepts.append(predictive_concept)
            if intuitive_concept not in new_concepts:
                new_concepts.append(intuitive_concept)

        return self.initially_proposed_concepts if new_concepts == [] else new_concepts

    def change_currently_used_concepts(self,
                                       explanation_type: str,
                                       new_values: list[str]
                                       ):
        if explanation_type not in {"decision_tree", "counterfactual"}:
            raise ValueError(f"Unknown explanation type: {explanation_type}")
        self.currently_used_concepts[explanation_type] = new_values

    def to_db_value(self) -> Dict[str, any]:
        return {
            'initially_proposed_concepts': self.initially_proposed_concepts,
            'most_predictive_concepts': self.most_predictive_concepts,
            'most_intuitive_concepts': self.most_intuitive_concepts,
            'currently_used_concepts': self.currently_used_concepts,
            'user_selected_concepts': self.user_selected_concepts,
        }

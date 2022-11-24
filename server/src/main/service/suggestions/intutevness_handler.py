from typing import List

from main.database.constraint_db import ConstraintDb
from main.database.intuitivness_db import IntuitivenessDb

DECISION_TREE = "decision_tree"
COUNTERFACTUAL = "counterfactual"


class UserSelectedConceptsHandler:
    def __init__(self):
        self.constraint_db = ConstraintDb()
        self.intuitiveness_db = IntuitivenessDb()

    def consept_suggestions(self,explanation_id: str,explanation_type: str,new_concepts: List[str]):

        if explanation_type not in {DECISION_TREE, COUNTERFACTUAL}:
            raise ValueError(f"Unknown explanation type: {explanation_type}")
        constraints = self.constraint_db.get_constraint_by_explanation_requirement_id(explanation_id)

        user_selected_concepts = constraints.user_selected_concepts[explanation_type]
        added_concepts = [concept for concept in new_concepts if concept not in user_selected_concepts]
        removed_concepts = [concept for concept in user_selected_concepts if concept not in new_concepts]

        for concept in added_concepts:
            new_value = self.intuitiveness_db.get_constraint_by_concept(concept).increment_count()
            self.intuitiveness_db.update_intuitiveness(new_value)
        for concept in removed_concepts:
            new_value = self.intuitiveness_db.get_constraint_by_concept(concept).decrement_count()
            self.intuitiveness_db.update_intuitiveness(new_value)

from typing import List, Optional

from main.database.constraint_db import ConstraintDb
from main.database.intuitivness_db import IntuitivenessDb
from main.models.enums import ExplanationType


class UserSelectedConceptsHandler:
    def __init__(self):
        self.constraint_db = ConstraintDb()
        self.intuitiveness_db = IntuitivenessDb()

    def consept_suggestions(self, explanation_id: str, explanation_type: ExplanationType, new_concepts: List[str]):

        constraints = self.constraint_db.get_constraint_by_explanation_requirement_id(explanation_id)

        user_selected_concepts = constraints.user_selected_concepts[explanation_type.value]
        added_concepts = [concept for concept in new_concepts if concept not in user_selected_concepts]
        removed_concepts = [concept for concept in user_selected_concepts if concept not in new_concepts]

        # TODO: these can be improved by query grouping
        for concept in added_concepts:
            new_value = self.intuitiveness_db.get_constraint_by_concept(concept).increment_count()
            self.intuitiveness_db.update_intuitiveness(new_value)
        for concept in removed_concepts:
            new_value = self.intuitiveness_db.get_constraint_by_concept(concept).decrement_count()
            self.intuitiveness_db.update_intuitiveness(new_value)

    def new_constraints_selected(self, explanation_id: str,
                                 constraint_type: str,
                                 explanation_type: Optional[ExplanationType],
                                 new_concepts: List[str]):
        constraints = self.constraint_db.get_constraint_by_explanation_requirement_id(explanation_id)
        constraints.change_concept_constraint(constraint_type, explanation_type, new_concepts)
        print(constraints.initially_proposed_concepts, flush=True)
        print(constraints.to_db_value(), flush=True)
        assert self.constraint_db.update_constraint(constraints) == True

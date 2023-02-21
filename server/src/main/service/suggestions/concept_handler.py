from typing import List, Optional

from main.database.constraint_db import ConstraintDb
from main.database.intuitivness_db import IntuitivenessDb
from main.models.enums import ExplanationType


class UserSelectedConceptsHandler:
    def __init__(self):
        self.constraint_db = ConstraintDb()
        self.intuitiveness_db = IntuitivenessDb()

    def initially_proposed_concepts(self,explanation_id: str, concepts: List[str]):
        constraints = self.constraint_db.get_constraint_by_explanation_requirement_id(explanation_id)
        constraints.change_concept_constraint("initially_proposed_concepts", ExplanationType.COUNTERFACTUAL, concepts)
        constraints.change_concept_constraint("initially_proposed_concepts", ExplanationType.DECISION_TREE, concepts)
        self.constraint_db.update_constraint(constraints)


    def consept_suggestions(self, explanation_id: str, explanation_type: ExplanationType, new_concepts: List[str]):
        raise NotImplementedError

        constraints = self.constraint_db.get_constraint_by_explanation_requirement_id(explanation_id)

        user_selected_concepts = constraints.user_selected_concepts[explanation_type.value]
        added_concepts = [concept for concept in new_concepts if concept not in user_selected_concepts]
        removed_concepts = [concept for concept in user_selected_concepts if concept not in new_concepts]

    def intuitive_concepts(self, explanation_id: str, explanation_type: ExplanationType,
                           label_intuitive_concepts_map: dict):
        raise NotImplementedError

    def new_constraints_selected(self, explanation_id: str,
                                 constraint_type: str,
                                 explanation_type: Optional[ExplanationType],
                                 new_concepts: List[str]):
        constraints = self.constraint_db.get_constraint_by_explanation_requirement_id(explanation_id)
        constraints.change_concept_constraint(constraint_type, explanation_type, new_concepts)
        self.constraint_db.update_constraint(constraints)

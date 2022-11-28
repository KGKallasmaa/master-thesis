import copy
import itertools
from typing import List, Set

from main.database.closest_labels import ClosestLabelsDb
from main.database.constraint_db import ConstraintDb
from main.database.explanation_requirement import ExplanationRequirementDb
from main.database.intuitivness_db import IntuitivenessDb
from main.models.consept_suggestions import ConceptSuggestions
from main.models.constraints import Constraints
from main.models.enums import ExplanationType
from main.service.pre_explanation.data_access import get_labels

TOP_K_PREDICTIVE_CONCEPTS = 5
TOP_K_INTUITIVE_CONCEPTS = 5
CONCEPT_SUGGESTION_LIMIT = 10


class ConceptSuggestionService:
    def __init__(self):
        self.constraint_db = ConstraintDb()
        self.intuitiveness_db = IntuitivenessDb()
        self.explanation_requirement_db = ExplanationRequirementDb()
        self.closest_labels_db = ClosestLabelsDb()

    def consept_suggestions(self, explanation_id: str, explanation_type: ExplanationType) -> ConceptSuggestions:

        constraints = self.constraint_db.get_constraint_by_explanation_requirement_id(explanation_id)
        explanation_requirement = self.explanation_requirement_db.get_explanation_requirement(explanation_id)
        image_label = get_labels()[explanation_requirement.original_image_id]
        print(constraints, flush=True)
        used_concepts = constraints.user_selected_concepts[explanation_type]

        if explanation_type == ExplanationType.DECISION_TREE:
            proposed_concepts = self.__propose_concepts_for_decision_tree(image_label=image_label,
                                                                          constraints=constraints)
        elif explanation_type == ExplanationType.COUNTERFACTUAL:
            proposed_concepts = self.__propose_concepts_for_counterfactual(
                image_id=explanation_requirement.original_image_id,
                image_label=image_label,
                constraints=constraints)
        else:
            raise ValueError("Unknown explanation type")

        print("used_concepts", flush=True)
        print(used_concepts, flush=True)
        print("availableToBeChosenConcepts", flush=True)
        print(proposed_concepts, flush=True)

        return ConceptSuggestions({
            "usedConcepts": used_concepts,
            "availableToBeChosenConcepts": proposed_concepts
        })

    def __propose_concepts_for_decision_tree(self, image_label: str, constraints: Constraints) -> List[str]:
        used_concepts = set(constraints.user_selected_concepts[ExplanationType.DECISION_TREE])
        most_predictive_concepts = constraints.most_predictive_concepts[ExplanationType.DECISION_TREE]
        most_predictive_concepts = [c for c in most_predictive_concepts if c not in used_concepts]

        most_intuitive_concepts = self.__most_intuitive_concepts(labels=[image_label], used_concepts=used_concepts)

        initially_proposed_concepts = set(constraints.initially_proposed_concepts)
        initially_proposed_concepts = initially_proposed_concepts.difference(set(used_concepts))

        return self.__combine_concepts(most_predictive_concepts=most_predictive_concepts,
                                       most_intuitive_concepts=most_intuitive_concepts,
                                       initially_proposed_concepts=list(initially_proposed_concepts))

    def __propose_concepts_for_counterfactual(self,
                                              image_id: int,
                                              image_label: str,
                                              constraints: Constraints) -> List[str]:
        used_concepts = set(constraints.user_selected_concepts[ExplanationType.COUNTERFACTUAL])

        most_predictive_concepts = constraints.most_predictive_concepts[ExplanationType.COUNTERFACTUAL]
        most_predictive_concepts = [c for c in most_predictive_concepts if c not in used_concepts]

        closest_labels = self.closest_labels_db.get_by_image_id(image_id)
        if closest_labels is None:
            most_intuitive_concepts = self.__most_intuitive_concepts(labels=[image_label], used_concepts=used_concepts)
        else:
            most_intuitive_concepts = self.__most_intuitive_concepts(labels=closest_labels.closest,
                                                                     used_concepts=used_concepts)

        initially_proposed_concepts = set(constraints.initially_proposed_concepts)
        initially_proposed_concepts = initially_proposed_concepts.difference(set(used_concepts))

        return self.__combine_concepts(most_predictive_concepts=most_predictive_concepts,
                                       most_intuitive_concepts=most_intuitive_concepts,
                                       initially_proposed_concepts=list(initially_proposed_concepts))

    def __most_intuitive_concepts(self, labels: List[str], used_concepts: Set[str]) -> List[str]:
        final_results = []

        for label in labels:
            intuitive_concepts = self.intuitiveness_db.top_intuitive_concepts(label, TOP_K_INTUITIVE_CONCEPTS)
            intuitive_concepts = [c.label for c in intuitive_concepts if c not in used_concepts]
            intuitive_concepts = [c for c in intuitive_concepts if c not in final_results]
            final_results.extend(intuitive_concepts)

        return final_results

    @staticmethod
    def __combine_concepts(
            most_predictive_concepts: List[str],
            most_intuitive_concepts: List[str],
            initially_proposed_concepts: List[str]) -> List[str]:

        proposed_concepts = []

        added_predictive_concepts, added_intuitive_concepts = set(), set()

        for combination in itertools.zip_longest(most_predictive_concepts, most_intuitive_concepts):
            if len(proposed_concepts) >= CONCEPT_SUGGESTION_LIMIT:
                return proposed_concepts[:CONCEPT_SUGGESTION_LIMIT]

            predictive_concept, intuitive_concept = combination

            should_append_predictive_concept = predictive_concept is not None and predictive_concept not in proposed_concepts and len(
                added_predictive_concepts) < TOP_K_PREDICTIVE_CONCEPTS
            if should_append_predictive_concept:
                proposed_concepts.append(predictive_concept)
                added_predictive_concepts.add(predictive_concept)

            should_append_intuitive_concept = intuitive_concept is not None and intuitive_concept not in proposed_concepts and len(
                added_intuitive_concepts) < TOP_K_INTUITIVE_CONCEPTS

            if should_append_intuitive_concept:
                proposed_concepts.append(intuitive_concept)
                added_intuitive_concepts.add(intuitive_concept)

        initially_proposed_concepts_copy = set(copy.copy(initially_proposed_concepts))
        initially_proposed_concepts_copy = initially_proposed_concepts_copy.difference(added_predictive_concepts)
        initially_proposed_concepts_copy = initially_proposed_concepts_copy.difference(added_intuitive_concepts)

        proposed_concepts.extend(list(initially_proposed_concepts_copy))

        return proposed_concepts[:CONCEPT_SUGGESTION_LIMIT] if len(proposed_concepts) > CONCEPT_SUGGESTION_LIMIT else proposed_concepts

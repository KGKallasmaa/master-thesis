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
    def __init__(self, constraint_db=ConstraintDb(),
                 intuitiveness_db=IntuitivenessDb(),
                 explanation_requirement_db=ExplanationRequirementDb(),
                 closest_labels_db=ClosestLabelsDb()):
        self.constraint_db = constraint_db
        self.intuitiveness_db = intuitiveness_db
        self.explanation_requirement_db = explanation_requirement_db
        self.closest_labels_db = closest_labels_db

    def consept_suggestions(self, explanation_id: str, explanation_type: ExplanationType) -> ConceptSuggestions:

        constraints = self.constraint_db.get_constraint_by_explanation_requirement_id(explanation_id)
        explanation_requirement = self.explanation_requirement_db.get_explanation_requirement(explanation_id)
        image_label = get_labels()[explanation_requirement.original_image_id]
        used_concepts = constraints.user_selected_concepts[explanation_type]

        match explanation_type:
            case ExplanationType.DECISION_TREE:
                proposed_concepts = self.__propose_concepts_for_decision_tree(image_label=image_label,
                                                                              constraints=constraints)
            case ExplanationType.COUNTERFACTUAL:
                proposed_concepts = self.__propose_concepts_for_counterfactual(
                    image_id=explanation_requirement.original_image_id,
                    image_label=image_label,
                    constraints=constraints)
            case _:
                raise Exception("Unknown explanation type")

        proposed_concepts = [c for c in proposed_concepts if c not in used_concepts]

        return ConceptSuggestions({
            "usedConcepts": used_concepts,
            "availableToBeChosenConcepts": proposed_concepts
        })

    def __propose_concepts_for_decision_tree(self, image_label: str, constraints: Constraints) -> List[str]:
        used_concepts = set(constraints.user_selected_concepts[ExplanationType.DECISION_TREE])
        most_predictive_concepts = constraints.most_predictive_concepts[ExplanationType.DECISION_TREE]
        most_predictive_concepts = [c for c in most_predictive_concepts if c not in used_concepts]

        most_intuitive_concepts = self.__most_intuitive_concepts(labels=[image_label])

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

        closest_labels = self.closest_labels_db.get_by_image_id(image_id)

        if closest_labels is None:
            most_intuitive_concepts = self.__most_intuitive_concepts(labels=[image_label])
        else:
            most_intuitive_concepts = self.__most_intuitive_concepts(labels=closest_labels.closest)

        most_predictive_concepts = [c for c in most_predictive_concepts if c not in used_concepts]
        most_intuitive_concepts = [c for c in most_intuitive_concepts if c not in used_concepts]

        return self.__combine_concepts(most_predictive_concepts=most_predictive_concepts,
                                       most_intuitive_concepts=most_intuitive_concepts,
                                       initially_proposed_concepts=constraints.initially_proposed_concepts)

    def __most_intuitive_concepts(self, labels: List[str]) -> List[str]:
        combined_most_intuitive_concepts = []

        for label in labels:
            intuitive_concepts = self.intuitiveness_db.top_intuitive_concepts(label, TOP_K_INTUITIVE_CONCEPTS)
            intuitive_concepts = [c.concept for c in intuitive_concepts]
            combined_most_intuitive_concepts.extend(intuitive_concepts)

        return list(dict.fromkeys(combined_most_intuitive_concepts))

    def __combine_concepts(
            self,
            most_predictive_concepts: List[str],
            most_intuitive_concepts: List[str],
            initially_proposed_concepts: List[str]) -> List[str]:

        proposed_concepts = []

        added_predictive_concepts, added_intuitive_concepts = set(), set()

        for combination in itertools.zip_longest(most_predictive_concepts, most_intuitive_concepts):
            if len(proposed_concepts) >= CONCEPT_SUGGESTION_LIMIT:
                return proposed_concepts[:CONCEPT_SUGGESTION_LIMIT]

            predictive_concept, intuitive_concept = combination

            if self.__should_append_predictive_concept(predictive_concept, proposed_concepts, added_intuitive_concepts):
                proposed_concepts.append(predictive_concept)
                added_predictive_concepts.add(predictive_concept)

            if self.__should_append_intuitive_concept(intuitive_concept, proposed_concepts, added_intuitive_concepts):
                proposed_concepts.append(intuitive_concept)
                added_intuitive_concepts.add(intuitive_concept)

        initially_proposed_concepts = [c for c in initially_proposed_concepts if c not in proposed_concepts]
        proposed_concepts.extend(initially_proposed_concepts)

        return proposed_concepts[:CONCEPT_SUGGESTION_LIMIT] if len(
            proposed_concepts) > CONCEPT_SUGGESTION_LIMIT else proposed_concepts

    @staticmethod
    def __should_append_intuitive_concept(intuitive_concept: str,
                                          proposed_concepts: List[str],
                                          added_intuitive_concepts: Set[str]):
        return intuitive_concept is not None and intuitive_concept not in proposed_concepts and len(
            added_intuitive_concepts) < TOP_K_INTUITIVE_CONCEPTS

    @staticmethod
    def __should_append_predictive_concept(predictive_concept: str,
                                           proposed_concepts: List[str],
                                           added_predictive_concepts: Set[str]):
        return predictive_concept is not None and predictive_concept not in proposed_concepts and len(
            added_predictive_concepts) < TOP_K_PREDICTIVE_CONCEPTS

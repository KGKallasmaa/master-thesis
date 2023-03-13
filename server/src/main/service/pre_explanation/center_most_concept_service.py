from typing import List, Dict, Set

from main.models.center_most_concept import CenterMostConcept
from main.service.pre_explanation.static_concepts_map import MOST_POPULAR_CONCEPTS, CENTER_MOST_CONCEPTS


def get_center_most_concepts(labels: List[str]) -> Dict[str, Dict[str, List[CenterMostConcept]]]:
    results: Dict[str, Dict[str, List[CenterMostConcept]]] = {}

    for label in labels:
        concepts = MOST_POPULAR_CONCEPTS.get(label, [])
        concepts: List[str] = [c for c in concepts if c in CENTER_MOST_CONCEPTS]

        concept_center_map = {}
        for concept in concepts:
            center_most_concepts: Set[CenterMostConcept] = CENTER_MOST_CONCEPTS.get(concept, set())
            current_center = concept_center_map.get(concept, set())
            concept_center_map[concept] = current_center.union(center_most_concepts)
        for key, value in concept_center_map.items():
            concept_center_map[key] = [c.to_db_value() for c in list(value)]
        results[label] = concept_center_map
    return results

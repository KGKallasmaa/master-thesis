from typing import List, Dict

from main.models.center_most_concept import CenterMostConcept
from main.service.pre_explanation.static_concepts_map import MOST_POPULAR_CONCEPTS, CENTER_MOST_CONCEPTS


class ConceptInClass:
    distanceToCenter: float
    src: str

    def __init__(self, distance_to_center: float, src: str):
        self.distanceToCenter = distance_to_center
        self.src = src

    def to_db_value(self) -> Dict[str, any]:
        return {
            'distanceToCenter': self.distanceToCenter,
            'src': self.src,
        }


class ImageConcept:
    name: str
    examples: List[ConceptInClass]

    def __init__(self, name: str):
        self.name = name
        self.examples = []

    def add_example(self, example: ConceptInClass):
        self.examples.append(example)
        self.examples.sort(key=lambda x: x.distanceToCenter)

    def add_examples(self, examples: List[ConceptInClass]):
        self.examples.extend(examples)
        self.examples.sort(key=lambda x: x.distanceToCenter)

    def to_db_value(self) -> Dict[str, any]:
        return {
            'name': self.name,
            'examples': [e.to_db_value() for e in self.examples],
        }


class CenterConceptInClass:
    label: str
    concepts: List[ImageConcept]

    def __init__(self, label: str, concepts: List[ImageConcept]):
        self.label = label
        self.concepts = concepts

    def to_db_value(self) -> Dict[str, any]:
        return {
            'label': self.label,
            'concepts': [c.to_db_value() for c in self.concepts],
        }


class CenterMostConceptsService:
    def get_center_most_concepts(self, labels: List[str]) -> List[CenterConceptInClass]:
        return [self.__get_center_most_concepts(label) for label in labels]

    @staticmethod
    def __get_center_most_concepts(label: str) -> CenterConceptInClass:
        image_concepts: List[ImageConcept] = []

        concepts = MOST_POPULAR_CONCEPTS.get(label, [])
        concepts: List[str] = [c for c in concepts if c in CENTER_MOST_CONCEPTS]

        for conceptName in concepts:
            image_concept = ImageConcept(conceptName)
            center_most_concepts: List[CenterMostConcept] = CENTER_MOST_CONCEPTS.get(conceptName, set())
            example_concepts: List[ConceptInClass] = [
                ConceptInClass(center_most_concept.distance, center_most_concept.src)
                for center_most_concept in center_most_concepts
            ]
            image_concept.add_examples(example_concepts)
            image_concepts.append(image_concept)

        return CenterConceptInClass(label, image_concepts)

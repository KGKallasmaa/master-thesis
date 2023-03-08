from multiprocessing import Manager
from multiprocessing.context import Process

from main.service.pre_explanation.center_concepts import CenterMostConceptsService
from main.service.pre_explanation.most_popular_concepts import MostPopularConcepts


def compute_center_most_concepts(center_most_concepts):
    center_most_concepts_service = CenterMostConceptsService()
    center_most_concepts.update(center_most_concepts_service.get_center_most_concept())


def compute_most_popular_concepts(most_popular_concepts):
    most_popular_concepts_service = MostPopularConcepts()
    most_popular_concepts.update(most_popular_concepts_service.static_most_popular_concepts())


def build_concepts():
    manager = Manager()
    center_most_concepts = manager.dict()
    most_popular_concepts = manager.dict()

    center_process = Process(target=compute_center_most_concepts, args=(center_most_concepts,))
    popular_process = Process(target=compute_most_popular_concepts, args=(most_popular_concepts,))

    center_process.start()
    popular_process.start()

    center_process.join()
    popular_process.join()

    return dict(center_most_concepts), dict(most_popular_concepts)


CENTER_MOST_CONCEPTS, MOST_POPULAR_CONCEPTS = build_concepts()

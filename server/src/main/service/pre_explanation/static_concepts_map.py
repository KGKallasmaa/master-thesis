from multiprocessing import Manager
from multiprocessing.context import Process

from main.service.pre_explanation.center_concepts import CenterMostConceptsService
from main.service.pre_explanation.data_access import get_labels
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

"""
Center most concepts example:
{
"office":{
    "chair": [
    {
    src:"https://www.google.com",
    distance: 0.5
    },
    ....
    ],
"""

print("Most popular concepts:")
print("Key type: ", type(MOST_POPULAR_CONCEPTS.keys()))
print("Value type: ", type(MOST_POPULAR_CONCEPTS.values()))
i = 0
for k, v in MOST_POPULAR_CONCEPTS.items():
    i += 1
    if i > 5:
        break
    print("label: ", k, "concepts: ", v)

print("Center most concepts:")
j = 0
print("Key type: ", type(CENTER_MOST_CONCEPTS.keys()))
print("Value type: ", type(CENTER_MOST_CONCEPTS.values()))
for k, v in CENTER_MOST_CONCEPTS.items():
    print("concept: ", k)
    j += 1
    if j > 5:
        break
    print("concept: ", k)
    for a, b in v.items():
        print(a, b, flush=True)


def bs_detector():
    label_mostpopular_concepts = {label: MOST_POPULAR_CONCEPTS.get(label, []) for label in set(get_labels())}
    ok_labels = []
    for label in set(get_labels()):
        concepts = [c for c in label_mostpopular_concepts[label] if c in CENTER_MOST_CONCEPTS]
        if concepts:
            ok_labels.append(label)
    return ok_labels


print("Labels with concepts:")
print(bs_detector())

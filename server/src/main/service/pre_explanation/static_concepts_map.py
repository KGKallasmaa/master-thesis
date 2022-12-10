from typing import Dict, List
from mpire import WorkerPool
from main.service.pre_explanation.data_access import get_masks, get_images, get_labels
from main.service.pre_explanation.most_popular_concepts import most_popular_concepts
import numpy as np
from functools import reduce


class MostPopularConcepts:
    BATCH_SIZE = 10
    MAX_WORKER_COUNT = 8

    def __init__(self):
        all_labels = np.array(list(set(get_labels())))
        chunk_size = max(1, int(all_labels.size / self.BATCH_SIZE))
        self.labels_in_chunks = np.array_split(all_labels, chunk_size)
        self.nr_of_jobs = min(self.MAX_WORKER_COUNT, len(self.labels_in_chunks))

        self.label_images_map = {}
        self.label_masks_map = {}

        self.image_most_popular_concepts = self.static_most_popular_concepts()

    def static_most_popular_concepts(self) -> Dict[str, List[any]]:
        for label, image, mask in zip(get_labels(), get_images(), get_masks()):
            current_images = self.label_images_map.get(label, [])
            current_maks = self.label_masks_map.get(label, [])

            current_images.append(image)
            current_maks.append(mask)

            self.label_images_map[label] = current_images
            self.label_masks_map[label] = current_maks

        with WorkerPool(n_jobs=self.nr_of_jobs) as pool:
            return reduce(lambda a, b: {**a, **b},
                          pool.map(self.__extract_most_popular_concepts, self.labels_in_chunks))

    def __extract_most_popular_concepts(self, labels: List[str]) -> Dict[str, List[any]]:
        partial_results = {}
        for label in labels:
            images = self.label_images_map[label]
            masks = self.label_masks_map[label]
            nr_of_images = len(images)
            partial_results[label] = most_popular_concepts(images, masks, nr_of_images)
        return partial_results

MOST_POPULAR_CONCEPTS = MostPopularConcepts().image_most_popular_concepts

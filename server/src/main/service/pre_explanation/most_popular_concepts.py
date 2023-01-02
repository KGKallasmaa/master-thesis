from main.service.pre_explanation.data_access import get_segments
from main.service.utils.dictionary import sort_dictionary

from typing import Dict, List
from mpire import WorkerPool
from main.service.pre_explanation.data_access import get_masks, get_images, get_labels
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
            partial_results[label] = self.most_popular_concepts(images, masks, nr_of_images)
        return partial_results

    @staticmethod
    def most_popular_concepts(images, masks, k) -> List[str]:
        segment_count = {}
        for pic, mask in zip(images, masks):
            _, seg_class = get_segments(np.array(pic), mask, threshold=0.005)
            for s in seg_class:
                segment_count[s] = segment_count.get(s, 0) + 1
        segment_count = sort_dictionary(segment_count)
        return [s for s, _ in segment_count[:k]]

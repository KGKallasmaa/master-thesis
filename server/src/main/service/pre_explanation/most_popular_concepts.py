import multiprocessing
from collections import defaultdict

from main.service.pre_explanation.data_access import get_segments
from main.service.utils.dictionary import sort_dictionary

from typing import Dict, List
from mpire import WorkerPool
from main.service.pre_explanation.data_access import get_masks, get_images, get_labels
import numpy as np
from functools import reduce

num_cpu_cores = multiprocessing.cpu_count()
BATCH_SIZE = 100
MAX_WORKER_COUNT = int(num_cpu_cores * (1 + (5 / num_cpu_cores)))


class MostPopularConcepts:
    def __init__(self):
        all_labels = np.array(list(set(get_labels())))
        chunk_size = max(1, int(all_labels.size / BATCH_SIZE))
        self.labels_in_chunks = np.array_split(all_labels, chunk_size)
        self.nr_of_jobs = min(MAX_WORKER_COUNT, len(self.labels_in_chunks))

        self.label_images_map = defaultdict(list)
        self.label_masks_map = defaultdict(list)

    def static_most_popular_concepts(self) -> Dict[str, List[any]]:
        for label, image, mask in zip(get_labels(), get_images(), get_masks()):
            self.label_images_map[label].append(image)
            self.label_masks_map[label].append(mask)

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

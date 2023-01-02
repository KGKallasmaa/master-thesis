from typing import List, Dict

from sklearn.cluster import KMeans

from main.models.center_most_concept import CenterMostConcept
from main.service.pre_explanation.common import array_to_image, resize_img, serve_pil_image, euclidean_distance
from main.service.pre_explanation.data_access import get_labels, get_images, get_masks, get_segments
from main.service.pre_explanation.most_popular_concepts import MostPopularConcepts
import numpy as np
from mpire import WorkerPool
from functools import reduce

TOP_SEGMENTS_COUNT = 10
TOP_EXAMPLES_COUNT = 5


class CenterMostConceptsService:
    BATCH_SIZE = 5
    MAX_WORKER_COUNT = 8

    """
              Every image (e.g. bedroom) is filled with segments (e.g bed, lamp, window).
              Our task is to give user top K(k=10) segments that best describe the image.
              1. We group images by label
              2. for each label we're going to cluster segments associated with them into k clusters
              3. and then for each segment we're going to return the l(l=5) sgements closest to each cluster center
    """

    def __init__(self):
        all_labels = np.array(list(set(get_labels())))
        chunk_size = max(1, int(all_labels.size / self.BATCH_SIZE))
        self.labels_in_chunks = np.array_split(all_labels, chunk_size)
        self.nr_of_jobs = min(self.MAX_WORKER_COUNT, len(self.labels_in_chunks))

        self.label_images = {}
        self.label_masks = {}
        self.center_most_concepts = self.__get_center_most_concept()

    def __get_center_most_concept(self) -> Dict[str, Dict[str, List[CenterMostConcept]]]:
        for label, image, mask in zip(get_labels(), get_images(), get_masks()):
            current_images = self.label_images.get(label, [])
            current_maks = self.label_masks.get(label, [])

            current_images.append(image)
            current_maks.append(mask)

            self.label_images[label] = current_images
            self.label_masks[label] = current_maks

        with WorkerPool(n_jobs=self.nr_of_jobs) as pool:
            return reduce(lambda a, b: {**a, **b},
                          pool.map(self.__partial_center_most_concepts,
                                   self.labels_in_chunks))

    def __partial_center_most_concepts(self, labels: List[str]) -> Dict[str, Dict[str, List[CenterMostConcept]]]:
        partial_results = {}
        for label in set(labels):
            images = self.label_images[label]
            masks = self.label_masks[label]
            k_means_segments = self.__kmeans(images, masks  )
            partial_results[label] = self.__sort_and_remove(k_means_segments)
        return partial_results

    @staticmethod
    def __kmeans(images, masks) -> List[CenterMostConcept]:
        all_segments = []
        segment_lookup = {}
        segment_labels = []

        most_pop_concepts = MostPopularConcepts.most_popular_concepts(images, masks, TOP_SEGMENTS_COUNT)
        for pic, mask in zip(images, masks):
            segss, seg_class = get_segments(np.array(pic), mask, threshold=0.005)
            for segment, segment_class in zip(segss, seg_class):
                if segment_class not in most_pop_concepts:
                    continue
                to_img = array_to_image(segment)
                segment = np.array(resize_img(to_img)).flatten()
                segment_lookup[str(segment)] = np.array(resize_img(to_img))
                all_segments.append(np.array(segment))
                segment_labels.append(segment_class)

        kmeans = KMeans(n_clusters=TOP_SEGMENTS_COUNT, random_state=0).fit(all_segments)

        results = []
        for label_index, segment in zip(kmeans.labels_, all_segments):
            results.append(CenterMostConcept({
                "conceptName": segment_labels[label_index],
                "src": serve_pil_image(array_to_image(segment_lookup[str(segment)])),
                "distance": euclidean_distance(kmeans.cluster_centers_[label_index], segment)
            }))
        return results

    @staticmethod
    def __sort_and_remove(k_means_segments: List[CenterMostConcept]) -> Dict[str, List[CenterMostConcept]]:
        concept_examples_map = {}
        for segment in k_means_segments:
            current_examples = concept_examples_map.get(segment.concept_name, [])
            current_examples.append(segment)
            concept_examples_map[segment.concept_name] = current_examples
        # we want to prevent duplicates. removing exact distance matches
        for concept, examples in concept_examples_map.items():
            examples.sort(key=lambda x: x.distance)
            used_distance_values = set()
            concept_examples = []
            for example in examples:
                if len(concept_examples) == TOP_EXAMPLES_COUNT:
                    break
                if example.distance not in used_distance_values:
                    concept_examples.append(example)
                    used_distance_values.add(example.distance)
            concept_examples_map[concept] = concept_examples
        return concept_examples_map

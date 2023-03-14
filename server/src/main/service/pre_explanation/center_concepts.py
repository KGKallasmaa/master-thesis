import multiprocessing
from collections import defaultdict
from typing import List, Dict, Set

from sklearn.cluster import KMeans

from main.models.center_most_concept import CenterMostConcept
from main.service.pre_explanation.common import array_to_image, resize_img, serve_pil_image, euclidean_distance
from main.service.pre_explanation.data_access import get_labels, get_images, get_masks, get_segments
from main.service.pre_explanation.most_popular_concepts import MostPopularConcepts
import numpy as np
from mpire import WorkerPool

num_cpu_cores = multiprocessing.cpu_count()
BATCH_SIZE = 200
MAX_WORKER_COUNT = int(num_cpu_cores * (1 + (3 / num_cpu_cores)))
TOP_SEGMENTS_COUNT = 10
TOP_EXAMPLES_COUNT = 5


class CenterMostConceptsService:
    """
              Every image (e.g. bedroom) is filled with segments (e.g bed, lamp, window).
              Our task is to give user top K(k=10) segments that best describe the image.
              1. We group images by label
              2. for each label we're going to cluster segments associated with them into k clusters
              3. and then for each segment we're going to return the l(l=5) sgements closest to each cluster center
    """

    def __init__(self):
        all_labels = np.array(list(set(get_labels())))
        chunk_size = max(1, int(all_labels.size / BATCH_SIZE))
        self.labels_in_chunks = np.array_split(all_labels, chunk_size)
        self.nr_of_jobs = min(MAX_WORKER_COUNT, len(self.labels_in_chunks))

        self.most_pop = MostPopularConcepts()

        self.label_images = {}
        self.label_masks = {}

    def get_center_most_concept(self) -> Dict[str, List[CenterMostConcept]]:
        for label, image, mask in zip(get_labels(), get_images(), get_masks()):
            current_images = self.label_images.get(label, [])
            current_images.append(image)
            self.label_images[label] = current_images

            current_masks = self.label_masks.get(label, [])
            current_masks.append(mask)
            self.label_masks[label] = current_masks

        with WorkerPool(n_jobs=self.nr_of_jobs) as pool:
            results = pool.map(self.__partial_center_most_concepts, self.labels_in_chunks)

        grouped_by_conceptname: Dict[str, Set[CenterMostConcept]] = {}
        for partial_results in results:
            for label, center_most_concepts_dict in partial_results.items():
                for concept, center_most_concepts in center_most_concepts_dict.items():
                    current_values = grouped_by_conceptname.get(concept, set())
                    grouped_by_conceptname[concept] = current_values.union(center_most_concepts)

        final_results: Dict[str, List[CenterMostConcept]] = {}

        for concept, center_most_concepts in grouped_by_conceptname.items():
            center_most_concepts = list(set(center_most_concepts))
            center_most_concepts.sort(key=lambda x: x.distance)
            final_results[concept] = center_most_concepts[:TOP_EXAMPLES_COUNT]

        return final_results

    def __partial_center_most_concepts(self, labels: List[str]) -> Dict[str, Dict[str, Set[CenterMostConcept]]]:
        return {
            label: self.__partial_center_most_concepts_for_label(label)
            for label in labels
        }

    def __partial_center_most_concepts_for_label(self, label: str) -> Dict[str, Set[CenterMostConcept]]:
        images = self.label_images[label]
        masks = self.label_masks[label]
        k_means_segments = self.__kmeans(images, masks)
        return self.__group_by_concept_name(k_means_segments)

    def __kmeans(self, images, masks) -> List[CenterMostConcept]:
        all_segments = []
        segment_lookup = {}
        segment_labels = []

        most_pop_concepts = self.most_pop.most_popular_concepts(images, masks, TOP_SEGMENTS_COUNT)
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
            results.append(CenterMostConcept(
                {"conceptName": segment_labels[label_index],
                 "src": serve_pil_image(array_to_image(segment_lookup[str(segment)])),
                 "distance": euclidean_distance(kmeans.cluster_centers_[label_index], segment)
                 })
            )
        return results

    @staticmethod
    def __group_by_concept_name(k_means_segments: List[CenterMostConcept]) -> Dict[str, Set[CenterMostConcept]]:
        concept_examples_map = defaultdict(set)
        for segment in k_means_segments:
            concept_examples_map[segment.concept_name].add(segment)
        return concept_examples_map

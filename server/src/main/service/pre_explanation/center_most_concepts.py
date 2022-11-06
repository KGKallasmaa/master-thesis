from typing import Dict, List

import numpy as np
from sklearn.cluster import KMeans

from main.service.pre_explanation.common import serve_pil_image, resize_img, array_to_image
from main.service.pre_explanation.data_access import get_masks, get_images, get_segments, get_labels
from main.service.pre_explanation.kmeans import euclidean_distance
from main.service.utils.dictionary import sort_dictionary


def center_most_concepts(k=10) -> Dict[str, List[any]]:
    """
    Every image (e.g. bedroom) is filled with segments (e.g bed, lamp, window).
    Our task is to give user top k(k=10) segments that best describe the image.
    1. We group images by label
    2. for each label we're going to cluster segments associated with them into n (where n is the number of unique segments)
    3. we're going to find k number of segments that are closest to their representative center
    """

    label_images = {}
    label_masks = {}

    for label, image, mask in zip(get_labels(), get_images(), get_masks()):
        current_images = label_images.get(label, [])
        current_maks = label_masks.get(label, [])

        current_images.append(image)
        current_maks.append(mask)

        label_images[label] = current_images
        label_masks[label] = current_maks
    # TODO: we should also extract concepst from coast and sea not only beach class
    return {
        label: kmean_segments(label_images[label], label_masks[label], k)
        for label in list(label_images.keys())
    }


def kmean_segments(images, masks, k=10):
    all_segments = []
    segment_lookup = {}
    segment_labels = []
    most_pop = most_popular_concepts(images, masks, k)
    for pic, mask in zip(images, masks):
        # TODO: we're feeding garbage into this
        segss, seg_class = get_segments(np.array(pic), mask, threshold=0.005)
        for segment, segment_class in zip(segss, seg_class):
            if segment_class not in most_pop:
                continue
            to_img = array_to_image(segment)
            segment = np.array(resize_img(to_img)).flatten()
            segment_lookup[str(segment)] = np.array(resize_img(to_img))
            all_segments.append(np.array(segment))
            segment_labels.append(segment_class)

    kmeans = KMeans(n_clusters=min(k, len(set(segment_labels))), random_state=0).fit(all_segments)

    segment_best_example_map = {}

    for label_index, segment in zip(kmeans.labels_, all_segments):
        segment_name = segment_labels[label_index]
        _, smallest_distance_to_center = segment_best_example_map.get(segment_name, (None, float('inf')))
        distance = euclidean_distance(kmeans.cluster_centers_[label_index], segment)
        if distance < smallest_distance_to_center:
            segment_as_arr = array_to_image(segment_lookup[str(segment)])
            segment_best_example_map[segment_name] = (serve_pil_image(segment_as_arr), distance)

    results = [
        {"conceptName": segment_name, "src": segment_value, "distance": smallest_distance_to_center}
        for segment_name, (segment_value, smallest_distance_to_center) in segment_best_example_map.items()
    ]

    results.sort(key=lambda x: x["distance"])

    return results


def most_popular_concepts(images, masks, k) -> List[str]:
    segment_count = {}
    for pic, mask in zip(images, masks):
        _, seg_class = get_segments(np.array(pic), mask, threshold=0.005)
        for s in seg_class:
            segment_count[s] = segment_count.get(s, 0) + 1
    segment_count = sort_dictionary(segment_count)
    return [s for s, _ in segment_count[:k]]


CENTER_MOST_CONCEPTS = center_most_concepts()

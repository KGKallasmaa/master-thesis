from typing import Dict, List

import numpy as np
from sklearn.cluster import KMeans

from main.service.pre_explanation.common import serve_pil_image, resize_img, array_to_image
from main.service.pre_explanation.data_access import get_masks, get_images, get_segments


def cluster_images(image_map, k=10) -> Dict[int, str]:
    image_val = list(image_map.values())

    resized_images = [resize_img(pic) for pic in image_val]
    resize_lookup = {str(resize): original for resize, original in zip(resized_images, image_map.values())}

    to_be_clustered_images = np.array([np.array(pic).flatten().tolist() for pic in resized_images])

    kmeans = KMeans(n_clusters=k, random_state=0).fit(to_be_clustered_images)

    clusterindex_images_map = {}

    for cluster_index, img in zip(kmeans.labels_, resized_images):
        current_values = clusterindex_images_map.get(cluster_index, [])
        current_values.append(img)
        clusterindex_images_map[cluster_index] = current_values

    bestimg_cluster = {}

    for cluster_index, images in clusterindex_images_map.items():
        cluster_center = kmeans.cluster_centers_[cluster_index]

        best_img = None
        best_distance = float('inf')

        for img in images:
            distance_from_center = euclidean_distance(cluster_center, np.array(img).flatten())
            if distance_from_center < best_distance:
                best_distance = distance_from_center
                best_img = img

        bestimg_cluster[cluster_index] = serve_pil_image(resize_lookup[str(best_img)])

    return bestimg_cluster


def concept_representatives(my_concept: str, k=5) -> List[any]:
    """
    Every image (e.g. bedroom) is filled with segments (e.g bed, lamp, window).
    Our task is to find k=5 best representatives from the given concept. E.g. we find the k top beds from our dataset
    """

    training_data = []
    segment_lookup = {}
    my_labels = []

    for pic, mask in zip(get_images(), get_masks()):
        segss, seg_class = get_segments(np.array(pic), mask, threshold=0.005)
        segss = [s for index, s in enumerate(segss) if seg_class[index] == my_concept]

        for s in segss:
            to_img = array_to_image(s)
            s = np.array(resize_img(to_img)).flatten()
            segment_lookup[str(s)] = np.array(resize_img(to_img))
            training_data.append(np.array(s))
            my_labels.append(my_concept)

    kmeans = KMeans(n_clusters=min(len(training_data), k), random_state=0).fit(training_data)

    label_index_segment_distance_map = {}
    for label_index, segment in zip(kmeans.labels_, training_data):
        distance = euclidean_distance(segment, kmeans.cluster_centers_[label_index])
        key = "{}___{}".format(label_index, segment)
        label_index_segment_distance_map[key] = distance

    label_index_segment_distance_map = dict(sorted(label_index_segment_distance_map.items(), key=lambda item: item[1]))

    i = 0
    results = []
    for key, distance in label_index_segment_distance_map.items():
        if i > k:
            continue
        i += 1
        label_index, segment = key.split("___")
        lookup = segment_lookup[str(segment)]
        segment_as_arr = array_to_image(lookup)
        results.append({"conceptName": my_concept, "src": serve_pil_image(segment_as_arr)})

    return results


def euclidean_distance(a: np.array, b: np.array, allow_not_equal=False) -> float:
    if allow_not_equal is False:
        assert a.shape == b.shape
        return np.linalg.norm(a - b)
    print("calculating euclidian distance for non equal size images. {} vs {}".format(a.shape, b.shape))
    a_number_of_rows, a_number_of_col = a.shape
    b_number_of_rows, b_number_of_col = b.shape

    rows, columns = min(a_number_of_rows, b_number_of_rows), min(a_number_of_col, b_number_of_col)
    a_copy = np.empty((rows, columns))
    b_copy = np.empty((rows, columns))

    for i in range(rows):
        a_copy[i] = a[i][:columns]
        b_copy[i] = b[i][:columns]
    return euclidean_distance(a_copy, b_copy)


def cosine_similarity(a: np.array, b: np.array) -> float:
    return np.dot(a, b) / (np.norm(a) * np.norm(b))

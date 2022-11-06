from typing import Dict

import numpy as np
from sklearn.cluster import KMeans

from main.service.pre_explanation.common import serve_pil_image, resize_img


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


def euclidean_distance(a: np.array, b: np.array, allow_not_equal=False) -> float:
    if a.shape == b.shape:
        return np.linalg.norm(a - b)
    if allow_not_equal is False:
        raise ValueError("Images must have the same shape")

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

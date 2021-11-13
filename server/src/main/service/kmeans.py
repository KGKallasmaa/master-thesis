from typing import Dict

import numpy as np
from sklearn.cluster import KMeans

from main.service.common import serve_pil_image, resize_img


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

        bestimg_cluster[cluster_index] = best_img

    for key, value in bestimg_cluster.items():
        bestimg_cluster[key] = serve_pil_image(resize_lookup[str(value)])
    return bestimg_cluster


def euclidean_distance(a: np.array, b: np.array) -> float:
    return np.linalg.norm(a - b)

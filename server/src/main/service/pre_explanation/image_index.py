import numpy as np

from main.service.pre_explanation.data_access import get_images
from main.service.pre_explanation.kmeans import euclidean_distance


def find_image_index(image: np.array) -> int:
    """Finding the closest index to the uploaded image"""
    to_be_compared_image_as_histogram = np.histogram(image.flatten(), bins=256, range=(0, 255))[0]
    all_images = get_images()
    index = -1
    best_distance = float('inf')
    for i, img in enumerate(all_images):
        img_as_array = np.array(img).flatten()
        image_as_histogram = np.histogram(img_as_array, bins=256, range=(0, 255))[0]
        distance = euclidean_distance(to_be_compared_image_as_histogram, image_as_histogram)
        if distance < best_distance:
            index = i
            best_distance = distance
    return index

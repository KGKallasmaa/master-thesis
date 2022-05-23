import numpy as np
import base64
from main.database.explanation_requirement import ExplanationRequirementDb
from main.service.pre_explanation.data_access import get_images
from main.service.pre_explanation.kmeans import euclidean_distance


def find_closest_image_index(image: np.array) -> int:
    """Finding the closest index to the uploaded user_uploaded_image"""
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


def attach_image_to_explanation(image: any, explanation_id: str):
    database = ExplanationRequirementDb()
    image_safe = base64.b64encode(image).decode("utf-8")
    database.add_original_image_to_explanation(image_safe, explanation_id)

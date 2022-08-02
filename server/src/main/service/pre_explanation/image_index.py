import numpy as np
from main.database.explanation_requirement import ExplanationRequirementDb
from main.service.pre_explanation.data_access import get_hog, HOGS
from main.service.pre_explanation.kmeans import euclidean_distance


def find_closest_image_index(image: np.array) -> int:
    """Finding the closest index to the uploaded user_uploaded_image"""
    target_image_hog = get_hog(image)
    index = -1
    best_distance = float('inf')
    for i, img_hog in enumerate(HOGS):
        distance = euclidean_distance(target_image_hog, img_hog, allow_not_equal=True)
        if distance == 0:
            return index
        if distance < best_distance:
            index = i
            best_distance = distance
    if index == -1:
        raise ValueError("Failed to find closest image")
    return index


def attach_image_to_explanation(image: str, explanation_id: str):
    database = ExplanationRequirementDb()
    database.add_original_image_to_explanation(image, explanation_id)

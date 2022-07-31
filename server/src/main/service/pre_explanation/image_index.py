import numpy as np
from src.main.database.explanation_requirement import ExplanationRequirementDb
from src.main.service.pre_explanation.data_access import get_images
from src.main.service.pre_explanation.kmeans import euclidean_distance
from skimage.feature import hog

def find_closest_image_index(image: np.array) -> int:
    """Finding the closest index to the uploaded user_uploaded_image"""
    target_image_hog = get_hog(image)
    index = -1
    best_distance = float('inf')
    for i, img in enumerate(get_images()):
        img_as_hog = get_hog(img)
        distance = euclidean_distance(target_image_hog, img_as_hog, allow_not_equal=True)
        if distance == 0:
            return index
        if distance < best_distance:
            index = i
            best_distance = distance
    if index == -1:
        raise ValueError("Failed to find closest image")
    return index


def get_hog(image: np.array):
    fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16),
                        cells_per_block=(1, 1), visualize=True, channel_axis=-1)
    return hog_image


def attach_image_to_explanation(image: str, explanation_id: str):
    database = ExplanationRequirementDb()
    database.add_original_image_to_explanation(image, explanation_id)

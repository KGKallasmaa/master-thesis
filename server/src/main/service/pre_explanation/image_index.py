import numpy as np
from src.main.database.explanation_requirement import ExplanationRequirementDb
from src.main.service.pre_explanation.data_access import get_images
from src.main.service.pre_explanation.kmeans import euclidean_distance
from skimage.feature import hog


def find_closest_image_index_old(image: np.array) -> int:
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


def find_closest_image_index(image: np.array) -> int:
    """Finding the closest index to the uploaded user_uploaded_image"""
    print("input image", flush=True)
    print(image.shape, flush=True)
    print(image[0], flush=True)
    target_image_hog = get_hog(image)
    print("are we here?")
    index = -1
    best_distance = float('inf')
    for i, img in enumerate(get_images()):
        img_as_hog = get_hog(img)
        distance = euclidean_distance(target_image_hog, img_as_hog, allow_not_equal=True)
        if distance < best_distance:
            index = i
            best_distance = distance
        if distance == 0:
            return index
    return index


def get_hog(image: np.array):
    return hog(image,
               orientations=8,
               pixels_per_cell=(16, 16),
               cells_per_block=(1, 1))


def attach_image_to_explanation(image: str, explanation_id: str):
    database = ExplanationRequirementDb()
    database.add_original_image_to_explanation(image, explanation_id)

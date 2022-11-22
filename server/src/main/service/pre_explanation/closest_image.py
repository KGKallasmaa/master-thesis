import numpy as np

from main.database.closest_labels import ClosestLabelsDb
from main.models.closest_label import ClosestLabel
from main.service.pre_explanation.data_access import get_hog, get_images, get_labels
from main.service.pre_explanation.kmeans import euclidean_distance
from main.service.utils.dictionary import sort_dictionary

closest_label_repository = ClosestLabelsDb()

# TODO: speed up this method. it's very slow
def find_closest_image_index(image: np.array, k_closest=5) -> int:
    """Finding the closest index to the uploaded user_uploaded_image"""
    # k = how many images we're using for closeness
    target_image_hog = get_hog(image)

    image_index_distance_dict = {}
    image_index_label_dict = {}

    for i, (img, label) in enumerate(zip(get_images(), get_labels())):
        img_hog = get_hog(img)
        image_index_distance_dict[i] = euclidean_distance(target_image_hog, img_hog, allow_not_equal=True)
        image_index_label_dict[i] = label

    sorted_image_index_distance_dict = sort_dictionary(image_index_distance_dict, reverse=False, by_value=True)
    label_presence_count_dict = {}

    for image_index, _ in sorted_image_index_distance_dict[:k_closest]:
        label = image_index_label_dict[image_index]
        label_presence_count_dict[label] = label_presence_count_dict.get(label, 0) + 1

    sorted_label_presence_count_dict = sort_dictionary(label_presence_count_dict, by_value=True)
    most_popular_label = sorted_label_presence_count_dict[0][0]

    for image_index, _ in image_index_distance_dict.items():
        if image_index_label_dict[image_index] != most_popular_label:
            continue

        closest_label = ClosestLabel({
            "image_index": image_index,
            "label": most_popular_label,
            "closest": [label for label, _ in sorted_label_presence_count_dict[1:]]
        })
        closest_label_repository.update_closest_labels(closest_label)

        return image_index

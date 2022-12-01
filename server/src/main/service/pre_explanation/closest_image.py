import numpy as np
from threading import Thread
from main.database.closest_labels import ClosestLabelsDb
from main.models.closest_label import ClosestLabel
from main.service.pre_explanation.data_access import get_hog, get_images, get_labels
from main.service.pre_explanation.kmeans import euclidean_distance
from main.service.utils.dictionary import sort_dictionary
import multiprocessing
from multiprocessing import Pool
from typing import Dict

closest_label_repository = ClosestLabelsDb()
TOP_K_CLOSEST = 8


def find_closest_for_existing_images():
    image_array_str_map = {
        np.array2string(np.array(img)): np.array(img)
        for img in get_images()
    }
    print(
        f"Starting to find closest images to {len(image_array_str_map)} closest images [initially {len(get_images())}]",
        flush=True)
    with Pool(multiprocessing.cpu_count()) as p:
        p.map(find_closest_image_index, image_array_str_map.values())

    print("find_closest_for_existing_images completed")


# TODO: speed up this method. it's very slow
def find_closest_image_index(image: np.array, k_closest=TOP_K_CLOSEST) -> int:
    """Finding the closest index to the uploaded user_uploaded_image"""
    target_image_hog = get_hog(image)

    # TODO: parralise this. Also we need to only find distances to distint images
    image_index_distance_dict = {i: euclidean_distance(target_image_hog, get_hog(img), allow_not_equal=True)
                                 for i, img in enumerate(get_images())
                                 }
    sorted_image_index_distance_dict = sort_dictionary(image_index_distance_dict, reverse=False, by_value=True)

    image_index_label_dict = dict(enumerate(get_labels()))
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
        print(closest_label.to_db_value(), flush=True)
        closest_label_repository.update_closest_labels(closest_label)

        return image_index


def find_image_index_distance_dict(target_img) -> Dict[int, float]:
    target_image_hog = get_hog(target_img)

    image_index_distance_dict, image_str_distance_dict = {}, {}
    for i, img in enumerate(get_images()):
        image_as_array = np.array2string(np.array(img))
        if image_as_array in image_str_distance_dict:
            image_str_distance_dict[image_as_array] = euclidean_distance(target_image_hog, get_hog(img),
                                                                         allow_not_equal=True)
        image_index_distance_dict[i] = image_str_distance_dict[image_as_array]

    return image_index_distance_dict


thread = Thread(target=find_closest_for_existing_images)
thread.start()

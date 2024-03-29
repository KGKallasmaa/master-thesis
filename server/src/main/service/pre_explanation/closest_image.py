import hashlib

import numpy as np
from threading import Thread
from main.database.closest_labels import ClosestLabelsDb
from main.models.closest_label import ClosestLabel
from main.service.pre_explanation.common import euclidean_distance
from main.service.pre_explanation.data_access import get_hog, get_images, get_labels, get_hogs
from main.service.utils.dictionary import sort_dictionary
import multiprocessing
from multiprocessing import Pool
from typing import Dict

closest_label_repository = ClosestLabelsDb()
TOP_K_CLOSEST = 8

_all_images = get_images()
_hogs = get_hogs()
image_index_label_dict = dict(enumerate(get_labels()))

def find_closest_for_existing_images():
    image_array_str_map = {
        hashlib.sha1(np.array(img).view(np.uint8)).hexdigest(): np.array(img)
        for img in get_images()
    }
    par_count = min(multiprocessing.cpu_count(),5)
    print(
        f"Starting to find on {par_count} CPUs closest images to {len(image_array_str_map)} closest images [initially {len(get_images())}]",
        flush=True)
    with Pool(par_count) as p:
        p.map(find_closest_image_index, image_array_str_map.values())

    print("find_closest_for_existing_images completed")


# TODO: speed up this method. it's very slow
def find_closest_image_index(image: np.array, k_closest=TOP_K_CLOSEST) -> int:
    """Finding the closest index to the uploaded user_uploaded_image"""
    print("find_closest_image_index", flush=True)
    image_index_distance_dict = find_image_index_distance_dict(image)
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

        existing_closest_labels = closest_label_repository.get_by_image_id(image_index)
        existing_closest_labels = [] if existing_closest_labels is None else existing_closest_labels.closest

        new_closest_labels = [label for label, _ in sorted_label_presence_count_dict[1:]]
        if len(new_closest_labels) == 0:
            continue

        if lists_have_same_elements(existing_closest_labels, new_closest_labels):
            return image_index

        new_closest_labels.extend(existing_closest_labels)
        new_closest_labels = list(dict.fromkeys(new_closest_labels))
        if len(new_closest_labels) > k_closest:
            new_closest_labels = new_closest_labels[:k_closest]
        new_closest_label_obj = ClosestLabel({
            "image_index": image_index,
            "label": most_popular_label,
            "closest": new_closest_labels
        })
        print(new_closest_label_obj.to_db_value(), flush=True)
        closest_label_repository.update_closest_labels(new_closest_label_obj)
        return image_index

    return -1


def lists_have_same_elements(list1, list2):
    return set(list1) == set(list2)


def find_image_index_distance_dict(target_img) -> Dict[int, float]:
    target_image_hog = get_hog(target_img)

    image_index_distance_dict, image_str_distance_dict = {}, {}
    for i, img in enumerate(_all_images):
        image_key = hashlib.sha1(np.array(img).view(np.uint8)).hexdigest()
        if image_key not in image_str_distance_dict:
            image_str_distance_dict[image_key] = euclidean_distance(target_image_hog, _hogs[i],
                                                                    allow_not_equal=True)
        image_index_distance_dict[i] = image_str_distance_dict[image_key]

    return image_index_distance_dict


find_closest_for_existing_images()
#thread = Thread(target=find_closest_for_existing_images)
#thread.start()
#thread.join()
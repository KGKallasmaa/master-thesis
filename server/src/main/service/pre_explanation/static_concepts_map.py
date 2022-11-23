from typing import Dict, List

from main.service.pre_explanation.data_access import get_masks, get_images, get_labels
from main.service.pre_explanation.kmeans import kmean_segments, most_popular_concepts

# TODO: apply multi processing https://www.machinelearningplus.com/python/parallel-processing-python/
def center_most_concepts(k=10) -> Dict[str, List[any]]:
    """
    Every image (e.g. bedroom) is filled with segments (e.g bed, lamp, window).
    Our task is to give user top k(k=10) segments that best describe the image.
    1. We group images by label
    2. for each label we're going to cluster segments associated with them into n (where n is the number of unique segments)
    3. we're going to find k number of segments that are closest to their representative center
    """

    label_images = {}
    label_masks = {}

    for label, image, mask in zip(get_labels(), get_images(), get_masks()):
        current_images = label_images.get(label, [])
        current_maks = label_masks.get(label, [])

        current_images.append(image)
        current_maks.append(mask)

        label_images[label] = current_images
        label_masks[label] = current_maks
    # TODO: we should also extract concept from coast and sea not only beach class
    return {
        label: kmean_segments(label_images[label], label_masks[label], k)
        for label in list(label_images.keys())
    }


def static_most_popular_concepts() -> Dict[str, List[any]]:
    label_images_map = {}
    label_masks_map = {}
    for label, image, mask in zip(get_labels(), get_images(), get_masks()):
        current_images = label_images_map.get(label, [])
        current_maks = label_masks_map.get(label, [])

        current_images.append(image)
        current_maks.append(mask)

        label_images_map[label] = current_images
        label_masks_map[label] = current_maks

    image_most_popular_concepts = {}
    for label in set(get_labels()):
        images = label_images_map[label]
        masks = label_masks_map[label]
        nr_of_images = len(images)  # TODO:maybe use set
        image_most_popular_concepts[label] = most_popular_concepts(images, masks, nr_of_images)

    return image_most_popular_concepts

LABEL_CENTER_MOST_CONCEPT = center_most_concepts()
MOST_POPULAR_CONCEPTS = static_most_popular_concepts()

from typing import Optional, Tuple, List

from main.service.common import serve_pil_image, base64_hash
from main.service.data_access import get_labels, get_images
from main.service.kmeans import cluster_images


def label_example_image(label: str) -> Tuple[int, Optional[str]]:
    for i, available_label in enumerate(get_labels()):
        if available_label == label:
            example_img = get_images()[i]
            return i, serve_pil_image(example_img)
    return -1, None


def label_all_images(label: str) -> List[any]:
    all_images = get_images()
    image_lookup = {
        i: all_images[i]
        for i, available_label in enumerate(get_labels())
        if available_label == label
    }

    cluster_image_result = cluster_images(image_lookup)

    return [{"hash": base64_hash(img), "src": img} for index, img in cluster_image_result.items()]

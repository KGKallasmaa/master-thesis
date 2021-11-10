from typing import Optional, Tuple, List

from service.common import serve_pil_image
from service.data_access import get_labels, get_images


def label_example_image(label: str) -> Tuple[int, Optional[str]]:
    for i, available_label in enumerate(get_labels()):
        if available_label == label:
            example_img = get_images()[i]
            return i, serve_pil_image(example_img)
    return -1, None


def label_all_images(label: str) -> List[any]:
    all_images = get_images()
    results = []
    for i, available_label in enumerate(get_labels()):
        if available_label == label:
            img = all_images[i]
            results.append({
                "index": i,
                "src": serve_pil_image(img)
            })
    return results

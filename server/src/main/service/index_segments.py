from typing import List

import numpy as np
from PIL import Image

from main.service.common import serve_pil_image
from main.service.data_access import get_images, get_masks, get_segments


def image_segments(index: int) -> List[any]:
    img_segments = []
    img_segments_classes = []
    i = 0
    for img, msk in zip(get_images(), get_masks()):
        if i != index:
            i += 1
            continue
        i += 1
        segss, seg_class = get_segments(np.array(img), msk, threshold=0.005)
        img_segments_classes.append(seg_class)
        img_segments.append(segss)

    results = []

    for img_seg in img_segments:
        for j, img in enumerate(img_seg):
            pil_image = Image.fromarray(np.uint8(img)).convert('RGB')
            results.append({
                "conceptName": img_segments_classes[0][j],
                "src": serve_pil_image(pil_image)
            })

    return results

from typing import List

import numpy as np
from PIL import Image

from main.service.pre_explanation.common import serve_pil_image
from main.service.pre_explanation.data_access import get_images, get_masks, get_segments

def image_segments(index: int) -> List[any]:
    img, msk = get_images()[index], get_masks()[index]
    segss, seg_class = get_segments(np.array(img), msk, threshold=0.005)

    return [
        {
            "conceptName": seg_class[i],
            "src": serve_pil_image(Image.fromarray(np.uint8(imgg)).convert('RGB'))
        }
        for i, imgg in enumerate(segss)
    ]



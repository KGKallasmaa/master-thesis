from typing import List

import numpy as np
from main.service.pre_explanation.data_access import get_segments
from main.service.utils.dictionary import sort_dictionary


def most_popular_concepts(images, masks, k) -> List[str]:
    segment_count = {}
    for pic, mask in zip(images, masks):
        _, seg_class = get_segments(np.array(pic), mask, threshold=0.005)
        for s in seg_class:
            segment_count[s] = segment_count.get(s, 0) + 1
    segment_count = sort_dictionary(segment_count)
    return [s for s, _ in segment_count[:k]]

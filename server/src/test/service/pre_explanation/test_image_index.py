import unittest

from src.main.service.pre_explanation.data_access import get_images
from src.main.service.pre_explanation.image_index import find_closest_image_index
import numpy as np

def test_works_with_same_image():
    # given
    target_image = np.array(get_images()[5])
    # when
    closest_image_index = find_closest_image_index(target_image)
    # then
    assert 5 == closest_image_index
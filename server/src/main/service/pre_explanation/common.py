import base64
from io import BytesIO

import PIL
import numpy as np
from PIL import Image


def serve_pil_image(img: PIL) -> str:
    img_buffer = BytesIO()
    img.save(img_buffer, format='JPEG')
    byte_data = img_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str.decode("utf-8")


def array_to_image(ar: np.array) -> PIL:
    return Image.fromarray(np.uint8(ar)).convert('RGB')


def resize_img(img, width=100, height=100) -> PIL:
    return img.resize((width, height), Image.ANTIALIAS)


def base64_to_pil(base64_str: str) -> PIL:
    image = base64.b64decode(base64_str)
    image = BytesIO(image)
    image = Image.open(image)
    return image


def euclidean_distance(a: np.array, b: np.array, allow_not_equal=False) -> float:
    if a.shape == b.shape:
        return np.linalg.norm(a - b)
    if allow_not_equal is False:
        raise ValueError("Images must have the same shape")

    a_number_of_rows, a_number_of_col = a.shape
    b_number_of_rows, b_number_of_col = b.shape

    rows, columns = min(a_number_of_rows, b_number_of_rows), min(a_number_of_col, b_number_of_col)
    a_copy = np.empty((rows, columns))
    b_copy = np.empty((rows, columns))

    for i in range(rows):
        a_copy[i] = a[i][:columns]
        b_copy[i] = b[i][:columns]
    return euclidean_distance(a_copy, b_copy)

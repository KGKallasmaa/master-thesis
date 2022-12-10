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

def base64_to_pil(base64_str: str) -> PIL:
    image = base64.b64decode(base64_str)
    image = BytesIO(image)
    image = Image.open(image)
    return image


def euclidean_distance(a: np.array, b: np.array, allow_not_equal=False) -> float:
    if a.shape == b.shape:
        return np.linalg.norm(a - b)
    if allow_not_equal is False:
        raise ValueError(f"Images must have the same shape. a.shape: {a.shape}, b.shape: {b.shape}")

    a_number_of_rows, a_number_of_col = a.shape
    b_number_of_rows, b_number_of_col = b.shape

    rows, columns = min(a_number_of_rows, b_number_of_rows), min(a_number_of_col, b_number_of_col)

    if a_number_of_rows != rows or a_number_of_col != columns:
        a = np.resize(a, (rows, columns))
    if b_number_of_rows != rows or b_number_of_col != columns:
        b = np.resize(b, (rows, columns))

    return euclidean_distance(a, b)

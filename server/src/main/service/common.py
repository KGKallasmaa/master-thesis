import base64
from io import BytesIO
import numpy as np
import PIL
import hashlib
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


def base64_hash(img: str) -> str:
    result = hashlib.md5(img.encode())
    return result.hexdigest()

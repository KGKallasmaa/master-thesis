import base64
from io import BytesIO

import PIL


def serve_pil_image(img: PIL) -> str:
    img_buffer = BytesIO()
    img.save(img_buffer, format='JPEG')
    byte_data = img_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str.decode("utf-8")

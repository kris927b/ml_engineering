import base64
from io import BytesIO
import json


def convert_to_base64(image_bytes: bytes):
    """
    Convert PIL images to Base64 encoded strings

    :param image_path: Path to image
    :return: Re-sized Base64 string
    """

    buffered = BytesIO(image_bytes)
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


def convert_string_to_json(str_input: str) -> dict:
    clean_str = str_input.replace("json", "").replace("\n", "").replace("`", "")
    return json.loads(clean_str)

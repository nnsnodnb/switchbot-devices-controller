import base64
import hashlib


def get_digest(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def get_b64encoded_digest(data: bytes) -> str:
    return base64.b64encode(get_digest(data)).decode()

import io
import pydantic
from PIL import Image


class StubRequest(pydantic.BaseModel):
    datas: str
    tokenInfo: str
    options: str


def read_image(b) -> Image:
    """Cast a byte array to a PIL.Image object"""
    return Image.open(io.BytesIO(b))

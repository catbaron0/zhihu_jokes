from dataclasses import dataclass
from typing import Optional



@dataclass
class ImageMessage:
    image_src: str
    caption: Optional[str]


@dataclass
class Article:
    title: str
    url: str

from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class ShortUrl(BaseModel):
    short_url: str
    original_url: str


class CreateShortUrl(BaseModel):
    url: str


class ShortUrlStatic(ShortUrl):
    use: int

    



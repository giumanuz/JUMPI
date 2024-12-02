from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Image:
    caption: str
    page: int
    data: bytes

@dataclass
class Article:
    title: str
    author: str
    content: str
    page_offsets: list[int]
    page_range: list[int] = field(default_factory=list)
    images: list[Image] = field(default_factory=list)

@dataclass
class Magazine:
    name: str
    year: int
    publisher: str
    genre: Optional[str] = None
    abstract: Optional[str] = None
    articles: list[Article] = field(default_factory=list)
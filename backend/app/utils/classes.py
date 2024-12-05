from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ArticlePageScan:
    page: int
    image_data: str
    uploaded_on: datetime


@dataclass
class ArticleFigure:
    page: int
    caption: str
    image_data: str


@dataclass
class Article:
    id: str
    magazine_id: str
    title: str
    author: str
    content: str
    page_offsets: list[int]
    page_range: list[int]
    page_scans: list[ArticlePageScan]
    figures: list[ArticleFigure] = field(default_factory=list)
    created_on: datetime = field(default_factory=lambda: datetime.now())
    edited_on: datetime = field(default_factory=lambda: datetime.now())

    @classmethod
    def placeholder_with(cls, **kwargs):
        return cls(
            id=kwargs.get('id', ''),
            magazine_id=kwargs.get('magazine_id', ''),
            title=kwargs.get('title', ''),
            author=kwargs.get('author', ''),
            content=kwargs.get('content', ''),
            page_offsets=kwargs.get('page_offsets', []),
            page_range=kwargs.get('page_range', []),
            page_scans=kwargs.get('page_scans', []),
            figures=kwargs.get('figures', []),
            created_on=kwargs.get('created_on', datetime.now()),
            edited_on=kwargs.get('updated_on', datetime.now())
        )


@dataclass
class Magazine:
    id: str
    name: str
    date: datetime
    publisher: str
    edition: Optional[str] = None
    abstract: Optional[str] = None
    genres: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)
    created_on: datetime = field(default_factory=lambda: datetime.now())
    edited_on: datetime = field(default_factory=lambda: datetime.now())

    @classmethod
    def placeholder_with(cls, **kwargs):
        return cls(
            id=kwargs.get('id', ''),
            name=kwargs.get('name', ''),
            date=kwargs.get('date', datetime.now()),
            publisher=kwargs.get('publisher', ''),
            edition=kwargs.get('edition', ''),
            abstract=kwargs.get('abstract', ''),
            genres=kwargs.get('genres', []),
            categories=kwargs.get('categories', []),
            created_on=kwargs.get('created_on', datetime.now()),
            edited_on=kwargs.get('updated_on', datetime.now())
        )

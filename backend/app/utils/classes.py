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

    # noinspection PyTypeChecker
    @classmethod
    def blank_with(cls, **kwargs):
        return cls(
            id=kwargs.get('id', None),
            magazine_id=kwargs.get('magazine_id', None),
            title=kwargs.get('title', None),
            author=kwargs.get('author', None),
            content=kwargs.get('content', None),
            page_offsets=kwargs.get('page_offsets', None),
            page_range=kwargs.get('page_range', None),
            page_scans=kwargs.get('page_scans', None),
            figures=kwargs.get('figures', None),
            created_on=kwargs.get('created_on', None),
            edited_on=kwargs.get('updated_on', None)
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

    # noinspection PyTypeChecker
    @classmethod
    def blank_with(cls, **kwargs):
        return cls(
            id=kwargs.get('id', None),
            name=kwargs.get('name', None),
            date=kwargs.get('date', None),
            publisher=kwargs.get('publisher', None),
            edition=kwargs.get('edition', None),
            abstract=kwargs.get('abstract', None),
            genres=kwargs.get('genres', None),
            categories=kwargs.get('categories', None),
            created_on=kwargs.get('created_on', None),
            edited_on=kwargs.get('updated_on', None)
        )

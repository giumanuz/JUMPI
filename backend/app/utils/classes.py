from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional


@dataclass
class ArticlePageScan:
    page: int
    image_data: str
    uploaded_on: datetime = field(default_factory=lambda: datetime.now())


@dataclass
class ArticleFigure:
    page: int
    caption: str
    image_data: str


@dataclass(init=False)
class _BaseEntity:
    # noinspection PyUnresolvedReferences,PyArgumentList
    @classmethod
    def __blank_with(cls, **kwargs):
        """Generic blank creation with specified kwargs."""
        blank_fields = {f.name: None for f in cls.__dataclass_fields__.values()}
        init_kwargs = {**blank_fields, **kwargs}
        return cls(**init_kwargs)

    @classmethod
    def create_blueprint_with(cls, **kwargs):
        """Create an instance for creation purposes."""
        kwargs['id'] = None
        kwargs['created_on'] = datetime.now()
        kwargs['edited_on'] = datetime.now()
        return cls(**kwargs)

    @classmethod
    def query_blueprint_with(cls, **kwargs):
        """Create an instance for query purposes."""
        return cls.__blank_with(**kwargs)

    @classmethod
    def update_blueprint_with(cls, **kwargs):
        """Create an instance for updates, setting `edited_on` to now."""
        kwargs['created_on'] = None
        kwargs['edited_on'] = datetime.now()
        return cls.__blank_with(**kwargs)

    # noinspection PyTypeChecker
    def to_dict(self):
        """Convert the dataclass to a dictionary."""
        dict_copy = asdict(self)
        return dict_copy        


@dataclass
class Article(_BaseEntity):
    id: str
    magazine_id: str
    title: str
    author: str
    page_range: list[int]
    page_scans: list[ArticlePageScan]
    content: str = ""
    page_offsets: list[int] = field(default_factory=list)
    figures: list[ArticleFigure] = field(default_factory=list)
    created_on: datetime = field(default_factory=lambda: datetime.now())
    edited_on: datetime = field(default_factory=lambda: datetime.now())


@dataclass
class Magazine(_BaseEntity):
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

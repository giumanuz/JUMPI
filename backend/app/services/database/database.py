from abc import ABC, abstractmethod

from app.utils.classes import Article, Magazine


class Database(ABC):
    @classmethod
    def set_instance(cls, instance) -> None:
        cls.instance = instance

    @classmethod
    def get_instance(cls) -> 'Database':
        return cls.instance

    @abstractmethod
    def ping(self) -> bool:
        ...

    @abstractmethod
    def add_magazine(self, magazine: Magazine) -> str:
        ...

    @abstractmethod
    def add_article(self, article: Article) -> str:
        ...

    @abstractmethod
    def get_all_magazines(self) -> list[Magazine]:
        ...

    @abstractmethod
    def search_magazines(self, magazine: Magazine) -> list[Magazine]:
        ...

    @abstractmethod
    def search_articles(self, article: Article) -> list[Article]:
        ...

    @abstractmethod
    def update_magazine(self, magazine: Magazine) -> None:
        ...

    @abstractmethod
    def update_article(self, article: Article) -> None:
        ...
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

    @abstractmethod
    def get_magazine(self, magazine_id: str) -> Magazine:
        ...

    @abstractmethod
    def get_article(self, article_id: str) -> Article:
        ...

    @abstractmethod
    def get_articles_from_magazine(self, magazine_id: str) -> list[Article]:
        ...

    @abstractmethod
    def query(self, magazine: Magazine, article: Article) -> list[Article]:
        ...

    @abstractmethod
    def exist_user(self, email: str) -> bool:
        ...

    @abstractmethod
    def login_user(self, email: str, password: str) -> bool:
        ...

    @abstractmethod
    def register_user(self, username: str, email: str, password: str) -> None:
        ...


class MagazineNotFoundError(Exception):
    pass


class MagazineExistsError(Exception):
    pass

from abc import ABC, abstractmethod

from database_utils.classes import Article, Magazine

class Database(ABC):
    @classmethod
    def set_instance(cls, instance):
        cls.instance = instance
    
    @classmethod
    def get_instance(cls) -> 'Database':
        return cls.instance

    @abstractmethod
    def connect(self) -> dict:
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        pass

    @abstractmethod
    def add_magazine(self, magazine) -> str:
        pass

    @abstractmethod
    def add_article(self, magazine, article) -> dict:
        pass

    @abstractmethod
    def get_magazine_id(self, magazine) -> str:
        pass

    @abstractmethod
    def magazine_exists(self, magazine) -> bool:
        pass

    @abstractmethod
    def query(self, magazine: Magazine, article: Article) -> dict:
        pass
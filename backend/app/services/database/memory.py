from app.services.database.database import Database, MagazineNotFoundError
from app.utils.classes import Article, Magazine


class InMemoryDb(Database):
    def __init__(self):
        self.magazines = []
        self.articles = []

    def ping(self) -> bool:
        return True

    def add_magazine(self, magazine: Magazine) -> str:
        id = len(self.magazines)
        self.magazines.append(magazine)
        return str(id)

    def add_article(self, article: Article) -> str:
        magazine_id = int(article.magazine_id)
        if not 0 <= magazine_id < len(self.magazines):
            raise MagazineNotFoundError
        id = len(self.articles)
        self.articles.append(article)
        return str(id)

    def get_all_magazines(self) -> list[Magazine]:
        return self.magazines.copy()

    def search_magazines(self, magazine: Magazine) -> list[Magazine]:
        return [magazine for magazine in self.magazines if magazine == magazine]

    def search_articles(self, article: Article) -> list[Article]:
        pass

    def update_magazine(self, magazine: Magazine) -> None:
        pass

    def update_article(self, article: Article) -> None:
        pass

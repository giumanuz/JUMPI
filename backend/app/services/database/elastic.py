import logging
from dataclasses import asdict

from elasticsearch import Elasticsearch
from flask import g

from app.utils.classes import Article, Magazine
from app.services.database.database import Database


def _build_magazine_search_query(magazine: Magazine) -> dict:
    return {
        "query": {"bool": {"must": [
            {"term": {"name": magazine.name}},
            {"range": {"year": {
                "gte": magazine.year,
                "lte": magazine.year
            }}},
            {"term": {"publisher": magazine.publisher}}
        ]}},
        "fields": ["_id"],
        "_source": False
    }


class ElasticsearchDb(Database):
    logger = logging.getLogger(__name__)

    def __init__(self, url):
        self.url = url

    @property
    def es(self):
        return Elasticsearch([self.url], api_key=g.api_key)

    def ping(self) -> bool:
        self.logger.error(self.es.info())
        return self.es.ping()

    def add_magazine(self, magazine: Magazine) -> str:
        if self.magazine_exists(magazine):
            raise MagazineExistsError
        return self._add_magazine_without_check(magazine)

    def _add_magazine_without_check(self, magazine: Magazine) -> str:
        magazine_dict = asdict(magazine)
        res = self.es.index(index='magazines', document=magazine_dict)
        self.__debug_log_query(magazine_dict, res.body)
        return res['_id']

    def add_article(self, magazine: Magazine, article: Article) -> dict:
        try:
            magazine_id = self.get_magazine_id(magazine)
        except MagazineNotFoundError:
            magazine_id = self.add_magazine(magazine)
        article_dict = asdict(article)

        query = {"script": {
            "source": "ctx._source.articles.add(params.new_article);",
            "params": {"new_article": article_dict}
        }}
        res = self.es.update(index="magazines", id=magazine_id, body=query)
        self.__debug_log_query(query, res.body)
        return res.body

    def get_magazine_id(self, magazine: Magazine) -> str:
        query = _build_magazine_search_query(magazine)
        res = self.es.search(index='magazines', body=query)
        self.__debug_log_query(query, res.body)
        if res['hits']['total']['value'] == 0:
            raise MagazineNotFoundError
        return res['hits']['hits'][0]['_id']

    def magazine_exists(self, magazine: Magazine) -> bool:
        try:
            self.get_magazine_id(magazine)
            return True
        except MagazineNotFoundError:
            return False

    def query(self, magazine: Magazine, article: Article) -> dict:
        query = {
            "query": {
                "bool": {
                    "filter": [],
                    "must": []
                }
            }
        }

        # Add optional filters for magazine-level fields
        for field in ("name", "year", "publisher", "genre"):
            value = getattr(magazine, field)
            if value:
                query["query"]["bool"]["filter"].append({"term": {field: value}})

        # Add nested article-level conditions if provided
        nested_conditions = {"filter": [], "must": []}

        if article.title:
            nested_conditions["filter"].append({"term": {"articles.title": article.title}})
        if article.author:
            nested_conditions["filter"].append({"term": {"articles.author": article.author}})
        if article.content:
            nested_conditions["must"].append({"match": {"articles.content": article.content}})

        # Add nested query only if there are conditions for articles
        if nested_conditions["filter"] or nested_conditions["must"]:
            query["query"]["bool"]["must"].append({
                "nested": {
                    "path": "articles",
                    "query": {
                        "bool": nested_conditions
                    }
                }
            })
        response = self.es.search(index="magazines", body=query)
        self.__debug_log_query(query, response.body)
        return response.body

    def __debug_log_query(self, query: dict, res: dict):
        self.logger.debug(
            f"""
            ----------------
            Query: {query}
            
            Response: {res}
            ----------------
            """
        )


class MagazineNotFoundError(Exception):
    pass


class MagazineExistsError(Exception):
    pass
import logging
from dataclasses import asdict

from elasticsearch import Elasticsearch
from flask import g

from database_utils.classes import Article, Magazine
from database_utils.database import Database


class ElasticsearchDb(Database):
    def __init__(self, url):
        self.url = url
        self.__es_base: Elasticsearch = None

    def connect(self) -> dict:
        self.__es_base = Elasticsearch([self.url])
        return self.__es_base.info().body

    def is_connected(self) -> bool:
        return self.__es_base.ping()

    @property
    def es(self):
        return self.__es_base.options(api_key=g.api_key)

    def add_magazine(self, magazine: Magazine) -> str:
        if self.magazine_exists(magazine):
            raise MagazineExistsError
        return self._add_magazine_without_check(magazine)

    def _add_magazine_without_check(self, magazine: Magazine) -> str:
        magazine_dict = asdict(magazine)
        res = self.es.index(index='magazines', document=magazine_dict)
        return res['_id']

    def add_article(self, magazine: Magazine, article: Article) -> dict:
        try:
            magazine_id = self.get_magazine_id(magazine)
        except MagazineNotFoundError:
            magazine_id = self.add_magazine(magazine)
        article_dict = asdict(article)

        return self.es.update(
            index="magazines",
            id=magazine_id,
            body={"script": {
                "source": "ctx._source.articles.add(params.new_article);",
                "params": {"new_article": article_dict}
            }}
        ).body

    def get_magazine_id(self, magazine: Magazine) -> str:
        query = self._build_magazine_search_query(magazine)
        res = self.es.search(index='magazines', body=query)
        if res['hits']['total']['value'] == 0:
            raise MagazineNotFoundError
        return res['hits']['hits'][0]['_id']

    def magazine_exists(self, magazine: Magazine) -> bool:
        try:
            self.get_magazine_id(magazine)
            return True
        except MagazineNotFoundError:
            return False

    def _build_magazine_search_query(self, magazine: Magazine) -> dict:
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

    def query(self, magazine: Magazine, article: Article) -> dict:
        # Initialize the base query
        query = {
            "query": {
                "bool": {
                    "filter": [],  # Exact match conditions go here
                    "must": []  # Full-text search conditions go here
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

        # Pretty-print the query
        logging.error(query)

        # Execute the query
        response = self.es.search(index="magazines", body=query)

        # Print the results
        print(response)

        return response.body


class MagazineNotFoundError(Exception):
    pass


class MagazineExistsError(Exception):
    pass

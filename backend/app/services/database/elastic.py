import logging
from dataclasses import asdict
from datetime import datetime
from typing import Iterable

from elasticsearch import Elasticsearch
from flask import g

from app.services.database.database import Database
from app.utils.classes import Article, Magazine, ArticlePageScan, ArticleFigure


class ElasticsearchDb(Database):
    logger = logging.getLogger(__name__)

    def __init__(self, url):
        self.url = url

    @property
    def es(self):
        return Elasticsearch([self.url], api_key=g.api_key)

    def ping(self) -> bool:
        self.logger.info(self.es.info())
        return self.es.ping()

    def add_magazine(self, magazine: Magazine) -> str:
        return self.__add_object(magazine, 'magazines')['_id']

    def add_article(self, article: Article) -> str:
        return self.__add_object(article, 'articles')['_id']

    def __add_object(self, obj, index):
        obj_dict = asdict(obj)
        obj_dict.pop('id')
        res = self.es.index(index=index, document=obj_dict).body
        self.__debug_log_query(obj_dict, res)
        return res

    def get_all_magazines(self) -> list[Magazine]:
        res = self.__search_object('magazines', {})
        return _parse_magazine_search_result(res)

    def search_magazines(self, magazine: Magazine) -> list[Magazine]:
        query = _get_search_magazine_query(magazine)
        res = self.__search_object('magazines', query)
        return _parse_magazine_search_result(res)

    def search_articles(self, article: Article) -> list[Article]:
        query = _get_search_article_query(article)
        res = self.__search_object('articles', query)
        return _parse_article_search_result(res)

    def __search_object(self, index, query):
        res = self.es.search(index=index, body=query).body
        self.__debug_log_query(query, res)
        return res

    def update_magazine(self, magazine: Magazine) -> bool:
        update_query = _get_update_magazine_query(magazine)
        res = self.es.update(
            index="magazines", id=magazine.id, body=update_query).body
        self.__debug_log_query(update_query, res)
        return res["result"] == "updated"

    def update_article(self, article: Article) -> bool:
        update_query = _get_update_article_query(article)
        res = self.es.update(
            index="articles", id=article.id, body=update_query).body
        self.__debug_log_query(update_query, res)
        return res["result"] == "updated"

    def get_magazine(self, magazine_id: str) -> Magazine:
        res = self.es.get(index="magazines", id=magazine_id).body['_source']
        return Magazine(id=magazine_id, **res)

    def get_article(self, article_id: str) -> Article:
        res = self.es.get(index="articles", id=article_id).body['_source']
        return Article(id=article_id, **res)

    def get_articles_from_magazine(self, magazine_id: str) -> list[Article]:
        article = Article.query_blueprint_with(magazine_id=magazine_id)
        query = _get_search_article_query(article)
        res = self.__search_object('articles', query)
        return _parse_article_search_result(res)

    # TODO: Da rivedere perche non è super clean
    def query(self, magazine: Magazine, article: Article) -> list[Article]:
        magazine_query = _get_search_magazine_query(magazine)

        res_magazines = self.es.search(
            index="magazines", body=magazine_query).body

        magazine_ids = [hit["_id"] for hit in res_magazines["hits"]
                        ["hits"]] if "hits" in res_magazines else []

        article_query = _get_search_article_query(article)
        if magazine_ids:
            article_query["query"]["bool"]["filter"] = [
                {"terms": {"magazine_id": magazine_ids}}
            ]

        res_articles = self.es.search(
            index="articles", body=article_query).body

        if "hits" not in res_articles or not res_articles["hits"]["hits"]:
            return []

        return _parse_article_search_result(res_articles)

    def __debug_log_query(self, query: dict, res: dict):
        self.logger.debug(
            f"""
            ----------------
            Query: {query}

            Response: {res}
            ----------------
            """
        )


def _parse_magazine_search_result(search_res: dict) -> list[Magazine]:
    magazines = []
    for hit in search_res["hits"]["hits"]:
        source = hit["_source"]
        magazine = Magazine(
            id=hit["_id"],
            name=source["name"],
            date=datetime.fromisoformat(source["date"]),
            publisher=source["publisher"],
            edition=source.get("edition"),
            abstract=source.get("abstract"),
            genres=source.get("genres", []),
            categories=source.get("categories", []),
            created_on=datetime.fromisoformat(source["created_on"]),
            edited_on=datetime.fromisoformat(source["edited_on"])
        )
        magazines.append(magazine)
    return magazines


def _parse_article_search_result(search_res: dict) -> list[Article]:
    articles = []

    for hit in search_res["hits"]["hits"]:
        source = hit["_source"]

        page_scans = [
            ArticlePageScan(
                page=page_scan["page"],
                image_data=page_scan["image_data"],
                uploaded_on=datetime.fromisoformat(page_scan["uploaded_on"])
            ) for page_scan in source.get("page_scans", [])
        ]

        figures = [
            ArticleFigure(
                page=figure["page"],
                caption=figure["caption"],
                image_data=figure["image_data"]
            ) for figure in source.get("figures", [])
        ]

        article = Article(
            id=hit["_id"],
            magazine_id=source["magazine_id"],
            title=source["title"],
            author=source["author"],
            content=source["content"],
            page_offsets=source.get("page_offsets", []),
            page_range=source.get("page_range", []),
            page_scans=page_scans,
            figures=figures,
            created_on=datetime.fromisoformat(source["created_on"]),
            edited_on=datetime.fromisoformat(source["edited_on"])
        )
        articles.append(article)

    return articles


def __get_search_query_with(obj_dict: dict, ignore_fields: Iterable[str], text_fields: Iterable[str]) -> dict:
    query = {}
    for field, value in obj_dict.items():
        if value is None or field in ignore_fields or not value:
            continue
        elif field in text_fields:
            query[field] = {"match": {field: value}}
        elif isinstance(value, list):
            query[field] = {"terms": {field: value}}
        elif isinstance(value, datetime):
            # TODO: Check if this is the correct way to handle dates.
            query[field] = {"term": {field: value.isoformat()}}
        else:
            query[field] = {"term": {field: value}}
    return {"query": {"bool": {"must": list(query.values())}}}


def __get_update_query_with(obj_dict: dict, ignore_fields: Iterable[str]) -> dict:
    update_fields = {}
    for field, value in obj_dict.items():
        if field == "id":
            continue
        if value is None or field in ignore_fields:
            continue
        if isinstance(value, datetime):
            update_fields[field] = value.isoformat()
        else:
            update_fields[field] = value
    return {"doc": update_fields}


_MAGAZINE_UPDATE_IGNORE_FIELDS = ("created_on",)
_ARTICLE_UPDATE_IGNORE_FIELDS = ("created_on",)


def _get_update_magazine_query(magazine: Magazine) -> dict:
    magazine_dict = asdict(magazine)
    return __get_update_query_with(magazine_dict, _MAGAZINE_UPDATE_IGNORE_FIELDS)


def _get_update_article_query(article: Article) -> dict:
    article_dict = asdict(article)
    return __get_update_query_with(article_dict, _ARTICLE_UPDATE_IGNORE_FIELDS)


_MAGAZINE_IGNORE_FIELDS = ("created_on", "edited_on")
_MAGAZINE_TEXT_FIELDS = ("abstract",)

_ARTICLE_IGNORE_FIELDS = ("page_scans", "figures",
                          "page_offsets", "page_range", "created_on", "edited_on")
_ARTICLE_TEXT_FIELDS = ("content",)


def _get_search_magazine_query(magazine: Magazine) -> dict:
    magazine_dict = asdict(magazine)
    return __get_search_query_with(magazine_dict, _MAGAZINE_IGNORE_FIELDS, _MAGAZINE_TEXT_FIELDS)


def _get_search_article_query(article: Article) -> dict:
    article_dict = asdict(article)
    return __get_search_query_with(article_dict, _ARTICLE_IGNORE_FIELDS, _ARTICLE_TEXT_FIELDS)

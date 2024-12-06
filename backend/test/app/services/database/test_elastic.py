from dataclasses import asdict
from datetime import datetime
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from app.services.database.elastic import ElasticsearchDb
from app.utils.classes import Magazine, Article


@pytest.fixture
def mock_es(mocker: MockerFixture):
    mock_es = MagicMock()
    mocker.patch('app.services.database.elastic.ElasticsearchDb.es', mock_es)
    return mock_es


@pytest.fixture
def mock_magazine_response(mock_magazine):
    mock_magazine_dict = asdict(mock_magazine)
    mock_magazine_dict["date"] = mock_magazine.date.isoformat()
    mock_magazine_dict["created_on"] = mock_magazine.created_on.isoformat()
    mock_magazine_dict["edited_on"] = mock_magazine.edited_on.isoformat()
    return {
        "hits": {
            "hits": [{
                "_id": "1",
                "_source": mock_magazine_dict
            }]
        }
    }


@pytest.fixture
def mock_article_response(mock_article):
    mock_article_dict = asdict(mock_article)

    mock_page_scan_dict = asdict(mock_article.page_scans[0])
    mock_page_scan_dict["uploaded_on"] = mock_article.page_scans[0].uploaded_on.isoformat()

    mock_figure_dict = asdict(mock_article.figures[0])

    mock_article_dict["created_on"] = mock_article.created_on.isoformat()
    mock_article_dict["edited_on"] = mock_article.edited_on.isoformat()
    mock_article_dict["page_scans"] = [mock_page_scan_dict]
    mock_article_dict["figures"] = [mock_figure_dict]
    return {
        "hits": {
            "hits": [{
                "_id": "1",
                "_source": mock_article_dict
            }]
        }
    }


def test_ping(mocker: MockerFixture):
    es_db = ElasticsearchDb(url="http://localhost:9200")
    mock_es = MagicMock()
    mocker.patch.object(ElasticsearchDb, 'es', mock_es)

    es_db.es.ping.return_value = True
    assert es_db.ping() is True

    es_db.es.ping.return_value = False
    assert es_db.ping() is False


def test_get_all_magazines(mock_es, mock_magazine_response, mock_magazine):
    mock_search_res = MagicMock()
    mock_search_res.body = mock_magazine_response
    mock_es.search.return_value = mock_search_res

    db = ElasticsearchDb(url="http://localhost")
    results = db.get_all_magazines()

    # Verify that Elasticsearch's search method is called
    mock_es.search.assert_called_once_with(index="magazines", body={})

    # Verify that the search result is correctly parsed into Magazine objects
    assert len(results) == 1
    assert results[0].id == "1"
    assert results[0].name == "Test Magazine"


# Test the add_magazine method
def test_add_magazine(mock_es, mock_magazine):
    mock_index_res = MagicMock()
    mock_index_res.body = {'_id': '1'}
    mock_es.index.return_value = mock_index_res

    db = ElasticsearchDb(url="http://localhost")
    magazine_id = db.add_magazine(mock_magazine)

    # Verify that Elasticsearch's index method is called
    mock_es.index.assert_called_once_with(index="magazines", document=asdict(mock_magazine))

    # Verify that the returned magazine ID is correct
    assert magazine_id == '1'


# Test the add_article method
def test_add_article(mock_es, mock_article):
    mock_index_res = MagicMock()
    mock_index_res.body = {'_id': '1'}
    mock_es.index.return_value = mock_index_res

    db = ElasticsearchDb(url="http://localhost")
    article_id = db.add_article(mock_article)

    # Verify that Elasticsearch's index method is called
    mock_es.index.assert_called_once_with(index="articles", document=asdict(mock_article))

    # Verify that the returned article ID is correct
    assert article_id == '1'


# Test the search_magazines method
def test_search_magazines(mock_es, mock_magazine_response, mock_magazine):
    mock_search_res = MagicMock()
    mock_search_res.body = mock_magazine_response
    mock_es.search.return_value = mock_search_res

    db = ElasticsearchDb(url="http://localhost")
    results = db.search_magazines(mock_magazine)

    # Verify the search query is passed to Elasticsearch
    query = {'query': {'bool': {'must': [{'term': {'id': '1'}},
                                         {'term': {'name': 'Test Magazine'}},
                                         {'term': {'date': '2024-01-01T00:00:00'}},
                                         {'term': {'publisher': 'Publisher A'}},
                                         {'term': {'edition': 'First Edition'}},
                                         {'match': {'abstract': 'Test abstract'}},
                                         {'terms': {'genres': ['genre1']}},
                                         {'terms': {'categories': ['cat1']}},
                                         {'term': {'edited_on': '2024-01-02T00:00:00'}}]}}}
    mock_es.search.assert_called_once_with(index="magazines", body=query)

    # Verify that the search result is correctly parsed into Magazine objects
    assert len(results) == 1
    assert results[0].id == "1"
    assert results[0].name == "Test Magazine"


def test_search_magazines_with_missing_fields(mock_es, mock_magazine_response, mock_magazine):
    mock_search_res = MagicMock()
    mock_search_res.body = mock_magazine_response
    mock_es.search.return_value = mock_search_res

    db = ElasticsearchDb(url="http://localhost")
    results = db.search_magazines(Magazine.query_blueprint_with(id="1"))

    # Verify the search query is passed to Elasticsearch
    query = {'query': {'bool': {'must': [{'term': {'id': '1'}}]}}}
    mock_es.search.assert_called_once_with(index="magazines", body=query)

    # Verify that the search result is correctly parsed into Magazine objects
    assert len(results) == 1
    assert results[0].id == "1"
    assert results[0].name == "Test Magazine"


def test_search_articles_with_missing_fields(mock_es, mock_article_response, mock_article):
    mock_search_res = MagicMock()
    mock_search_res.body = mock_article_response
    mock_es.search.return_value = mock_search_res

    db = ElasticsearchDb(url="http://localhost")
    results = db.search_articles(Article.query_blueprint_with(id="2", magazine_id="1"))

    # Verify the search query is passed to Elasticsearch
    query = {'query': {'bool': {'must': [{'term': {'id': '2'}},
                                         {'term': {'magazine_id': '1'}}]}}}
    mock_es.search.assert_called_once_with(index="articles", body=query)

    # Verify that the search result is correctly parsed into Article objects
    assert len(results) == 1
    assert results[0].id == "1"
    assert results[0].title == "Test Article"


# Test the search_articles method
def test_search_articles(mock_es, mock_article, mock_article_response):
    mock_search_res = MagicMock()
    mock_search_res.body = mock_article_response
    mock_es.search.return_value = mock_search_res

    db = ElasticsearchDb(url="http://localhost")
    results = db.search_articles(mock_article)

    # Verify the search query is passed to Elasticsearch
    query = {'query': {'bool': {'must': [{'term': {'id': '1'}},
                                         {'term': {'magazine_id': '1'}},
                                         {'term': {'title': 'Test Article'}},
                                         {'term': {'author': 'John Doe'}},
                                         {'match': {'content': 'Some content'}},
                                         {'term': {'edited_on': '2024-01-02T00:00:00'}}]}}}
    mock_es.search.assert_called_once_with(index="articles", body=query)

    # Verify that the search result is correctly parsed into Article objects
    assert len(results) == 1
    assert results[0].id == "1"
    assert results[0].title == "Test Article"


# Test the update_magazine method
def test_update_magazine(mock_es, mock_magazine):
    mock_update_res = MagicMock()
    mock_update_res.body = {"result": "updated"}
    mock_es.update.return_value = mock_update_res

    db = ElasticsearchDb(url="http://localhost")
    success = db.update_magazine(mock_magazine)

    # Verify that the update query is correctly formed and passed to Elasticsearch
    update_query = {'doc': {'abstract': 'Test abstract',
                            'categories': ['cat1'],
                            'date': '2024-01-01T00:00:00',
                            'edited_on': '2024-01-02T00:00:00',
                            'edition': 'First Edition',
                            'genres': ['genre1'],
                            'id': '1',
                            'name': 'Test Magazine',
                            'publisher': 'Publisher A'}}
    mock_es.update.assert_called_once_with(index="magazines", id="1", body=update_query)

    # Verify that the method returns True when successful
    assert success is True


# Test the update_article method
def test_update_article(mock_es, mock_article):
    mock_update_res = MagicMock()
    mock_update_res.body = {"result": "updated"}
    mock_es.update.return_value = mock_update_res

    db = ElasticsearchDb(url="http://localhost")
    success = db.update_article(mock_article)

    # Verify that the update query is correctly formed and passed to Elasticsearch
    update_query = {'doc': {'author': 'John Doe',
                            'content': 'Some content',
                            'edited_on': '2024-01-02T00:00:00',
                            'figures': [{'caption': 'Caption 1',
                                         'image_data': 'image_data_2',
                                         'page': 1}],
                            'id': '1',
                            'magazine_id': '1',
                            'page_offsets': [1, 2],
                            'page_range': [3, 4],
                            'page_scans': [{'image_data': 'image_data_1',
                                            'page': 1,
                                            'uploaded_on': datetime(2024, 1, 1, 0, 0)}],
                            'title': 'Test Article'}}
    mock_es.update.assert_called_once_with(index="articles", id="1", body=update_query)

    # Verify that the method returns True when successful
    assert success is True

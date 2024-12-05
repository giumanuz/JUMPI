import pytest
from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from app.services.database.elastic import ElasticsearchDb, Magazine, Article, MagazineNotFoundError, MagazineExistsError
from app import create_app

@pytest.fixture
def es_db(mocker: MockerFixture):
    """Fixture to create an instance of ElasticsearchDb with application context."""
    
    app = create_app()
    with app.app_context():
        es_db = ElasticsearchDb(url="http://localhost:9200")
        mock_es = MagicMock()
        mocker.patch.object(ElasticsearchDb, 'es', mock_es)
        yield es_db


def test_ping(es_db):
    """Test the ping method of ElasticsearchDb to ensure it correctly reflects Elasticsearch's availability."""
    es_db.es.ping.return_value = True
    assert es_db.ping() is True

    es_db.es.ping.return_value = False
    assert es_db.ping() is False


def test_add_magazine(es_db):
    """Test adding a magazine to ElasticsearchDb and ensure it returns the correct ID."""
    search_mock = MagicMock()
    search_mock.body = {'hits': {'total': {'value': 0}, 'hits': []}}
    es_db.es.search.return_value = search_mock

    index_mock = MagicMock()
    index_mock.body = {'_id': '12345', 'result': 'created'}
    index_mock.__getitem__.side_effect = lambda key: index_mock.body[key]
    es_db.es.index.return_value = index_mock

    es_db.magazine_exists = MagicMock(return_value=False)

    magazine = Magazine(name="Tech Monthly", year=2024, publisher="Tech Publisher")
    magazine_id = es_db.add_magazine(magazine)

    assert magazine_id == '12345'
    es_db.es.index.assert_called_once_with(index='magazines', document=vars(magazine))
    assert index_mock.body['_id'] == '12345'


def test_add_magazine_exists(es_db):
    """Test that adding a magazine that already exists raises a MagazineExistsError."""
    search_mock = MagicMock()
    search_mock.body = {
        'hits': {
            'total': {'value': 1},
            'hits': [{'_id': '12345'}]
        }
    }
    es_db.es.search.return_value = search_mock
    
    magazine = Magazine(name="Tech Monthly", year=2024, publisher="Tech Publisher")
    
    with pytest.raises(MagazineExistsError):
        es_db.add_magazine(magazine)


def test_get_magazine_id(es_db):
    """Test retrieving the ID of an existing magazine in ElasticsearchDb."""
    search_mock = MagicMock()
    search_mock.body = {
        'hits': {
            'total': {'value': 1},
            'hits': [{'_id': '12345'}]
        }
    }
    search_mock.__getitem__.side_effect = lambda key: search_mock.body[key]
    es_db.es.search.return_value = search_mock

    magazine = Magazine(name="Tech Monthly", year=2024, publisher="Tech Publisher")
    
    magazine_id = es_db.get_magazine_id(magazine)
    
    assert magazine_id == '12345'


def test_magazine_not_found_error(es_db):
    """Test that trying to retrieve a non-existent magazine raises a MagazineNotFoundError."""
    search_mock = MagicMock()
    search_mock.body = {'hits': {'total': {'value': 0}, 'hits': []}}
    search_mock.__getitem__.side_effect = lambda key: search_mock.body[key]
    es_db.es.search.return_value = search_mock

    magazine = Magazine(name="Non Existent Magazine", year=2024, publisher="Unknown Publisher")
    
    with pytest.raises(MagazineNotFoundError):
        es_db.get_magazine_id(magazine)


def test_query(es_db):
    """Test querying ElasticsearchDb with specific magazine and article filters."""
    search_mock = MagicMock()
    search_mock.body = {
        'hits': {
            'total': {'value': 1},
            'hits': [{'_id': '12345', '_source': {'name': 'Tech Monthly'}}]
        }
    }
    es_db.es.search.return_value = search_mock
    
    magazine = Magazine(name="Tech Monthly", year=2024, publisher="Tech Publisher")
    article = Article(title="AI Innovations", author="John Doe", content="Content of the article.", page_offsets=[])
    
    response = es_db.query(magazine, article)
    
    assert response['hits']['hits'][0]['_id'] == '12345'

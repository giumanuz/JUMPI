import pytest
from flask import Flask
from pytest_mock import MockerFixture

from app.routes.query import query_bp


@pytest.fixture
def app():
    """Fixture to create a Flask application for testing."""
    app = Flask(__name__)
    app.register_blueprint(query_bp)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Fixture to provide a test client for the Flask app."""
    return app.test_client()


@pytest.fixture
def mock_database_query(mocker: MockerFixture):
    """Fixture to mock the Database query method."""
    mock_db_instance = mocker.MagicMock()
    mocker.patch('app.services.database.database.Database.get_instance', return_value=mock_db_instance)
    return mock_db_instance


def test_query_documents_success(client, mock_database_query):
    """Test case when query parameters are passed and query is successful."""
    mock_database_query.query.return_value = {"magazines": ["mocked magazine"], "articles": ["mocked article"]}

    query_params = {
        'name_magazine': 'Test Magazine',
        'year': '2024',
        'publisher': 'Test Publisher',
        'genre': 'Science',
        'article_title': 'Test Article',
        'article_author': 'Test Author',
        'content': 'Test content'
    }

    response = client.get('/query', query_string=query_params)

    assert response.status_code == 200

    response_json = response.json
    assert "magazines" in response_json
    assert "articles" in response_json
    assert response_json["magazines"] == ["mocked magazine"]
    assert response_json["articles"] == ["mocked article"]

    mock_database_query.query.assert_called_once()

    args, kwargs = mock_database_query.query.call_args
    magazine_arg = args[0]
    article_arg = args[1]

    assert magazine_arg.name == 'Test Magazine'
    assert magazine_arg.year == '2024'
    assert magazine_arg.publisher == 'Test Publisher'
    assert magazine_arg.genre == 'Science'

    assert article_arg.title == 'Test Article'
    assert article_arg.author == 'Test Author'
    assert article_arg.content == 'Test content'


def test_query_documents_no_params(client, mock_database_query):
    """Test case when no query parameters are provided."""
    mock_database_query.query.return_value = {"magazines": [], "articles": []}

    response = client.get('/query')

    assert response.status_code == 200

    response_json = response.json
    assert "magazines" in response_json
    assert "articles" in response_json
    assert response_json["magazines"] == []
    assert response_json["articles"] == []

    mock_database_query.query.assert_called_once()

    args, kwargs = mock_database_query.query.call_args
    magazine_arg = args[0]
    article_arg = args[1]

    assert magazine_arg.name is None
    assert magazine_arg.year is None
    assert magazine_arg.publisher is None
    assert magazine_arg.genre is None

    assert article_arg.title is None
    assert article_arg.author is None
    assert article_arg.content is None

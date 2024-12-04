import json
import logging
from io import BytesIO

import pytest
from dotenv import load_dotenv
from flask import Flask
from pytest_mock import MockerFixture

from app.routes.analyze import analyze_bp

logging.basicConfig(level=logging.DEBUG)

load_dotenv()


@pytest.fixture
def app():
    """Fixture to create a Flask application for testing."""
    app = Flask(__name__)
    app.register_blueprint(analyze_bp)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Fixture to provide a test client for the Flask app."""
    return app.test_client()


@pytest.fixture
def mock_process_files(mocker: MockerFixture):
    """Fixture to mock the process_files function."""
    return mocker.patch('app.routes.analyze.process_files',
                        return_value=("mocked extracted text", [], []))


@pytest.fixture
def mock_database(mocker: MockerFixture):
    """Fixture to mock the Database interactions."""
    mock_db_instance = mocker.MagicMock()
    mocker.patch('app.routes.analyze.Database.get_instance',
                 return_value=mock_db_instance)
    return mock_db_instance


def test_analyze_documents_no_files(client):
    """Test case when no files are uploaded."""
    response = client.post('/analyze-documents', data={})
    assert response.status_code == 400
    assert response.json == {"error": "No files provided"}


def test_analyze_documents_empty_files(client):
    """Test case when files list is empty."""
    files = {}
    response = client.post('/analyze-documents', data=files)
    assert response.status_code == 400
    assert response.json == {"error": "No files provided"}


def test_analyze_documents_no_metadata(client):
    """Test case when metadata is missing."""
    files = {
        'files': (BytesIO(b"test file content"), 'test.pdf')
    }
    response = client.post('/analyze-documents', data=files)
    assert response.status_code == 400
    assert response.json == {"error": "Missing metadata"}


def test_analyze_documents_invalid_metadata_format(client):
    """Test case when the metadata JSON is malformed."""
    files = {
        'files': (BytesIO(b"test file content"), 'test.pdf')
    }
    data = {
        'metadata': 'invalid_json'
    }
    response = client.post('/analyze-documents', data={**files, **data})
    assert response.status_code == 400
    assert response.json == {"error": "Invalid metadata format"}


def test_analyze_documents_missing_metadata_field(client):
    """Test case when a required metadata field is missing."""
    files = {
        'files': (BytesIO(b"test file content"), 'test.pdf')
    }
    metadata = {
        'name_magazine': 'Test Magazine',
        'year': 2024,
        'publisher': 'Test Publisher',
        'genre': 'Test Genre',
        'article_title': 'Test Article',
        'article_author': 'Test Author'
        # Missing required field 'article_page_range'
    }
    data = {
        'metadata': json.dumps(metadata)
    }
    response = client.post('/analyze-documents', data={**files, **data})
    assert response.status_code == 400
    assert response.json == {"error": "Missing required field: article_page_range"}


def test_analyze_documents_success(
        client,
        mock_process_files,
        mock_database
):
    """Test case when all inputs are correct and processing is successful."""
    files = {
        'files': (BytesIO(b"test file content"), 'test.pdf')
    }
    metadata = {
        'name_magazine': 'Test Magazine',
        'year': 2024,
        'publisher': 'Test Publisher',
        'genre': 'Test Genre',
        'article_title': 'Test Article',
        'article_author': 'Test Author',
        'article_page_range': '1-10'
    }
    data = {
        'metadata': json.dumps(metadata)
    }

    response = client.post('/analyze-documents', data={**files, **data})

    assert response.status_code == 200

    response_json = response.json
    assert 'extracted_text' in response_json
    assert 'image_comparisons' in response_json
    assert response_json['extracted_text'] == "mocked extracted text"
    assert response_json['image_comparisons'] == []

    mock_process_files.assert_called_once()

    mock_database.add_article.assert_called_once()

    args = mock_database.add_article.call_args[0]
    assert args[0].name == 'Test Magazine'
    assert args[0].year == 2024
    assert args[1].title == 'Test Article'
    assert args[1].author == 'Test Author'
    assert args[1].page_range == [1, 10]

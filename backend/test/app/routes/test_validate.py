import pytest
from flask import Flask

from app.routes.validate import validate_bp
from app.services.database.database import Database


@pytest.fixture
def app():
    """Fixture to create a Flask application for testing."""
    app = Flask(__name__)
    app.register_blueprint(validate_bp)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Fixture to provide a test client for the Flask app."""
    return app.test_client()


def test_validate_api_key_success(client, mocker):
    """Test case when the database is available."""
    mocker.patch.object(Database, 'get_instance', return_value=mocker.MagicMock(ping=lambda: True))

    response = client.get('/validate-api-key')

    assert response.status_code == 200

    response_json = response.get_json()
    assert response_json == {"message": "API key is valid"}


def test_validate_api_key_failure(client, mocker):
    """Test case when the database is not available."""
    mocker.patch.object(Database, 'get_instance', return_value=mocker.MagicMock(ping=lambda: False))

    response = client.get('/validate-api-key')

    assert response.status_code == 500

    response_json = response.get_json()
    assert response_json == {"message": "Database is not available"}

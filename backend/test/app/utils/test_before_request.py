import pytest
from flask import Flask, g

from app.utils.before_request import setup_before_request


@pytest.fixture
def test_app():
    """Fixture to create and configure a Flask app for testing."""
    app = Flask(__name__)
    setup_before_request(app)

    @app.route('/test', methods=['GET', 'POST', 'OPTIONS'])
    def test_route():
        # Simple route to trigger `before_request`
        return {"message": "Success"}, 200

    return app


def test_load_user_api_key_options_request(test_app):
    """Test that OPTIONS requests bypass API key validation."""
    with test_app.test_client() as client:
        response = client.options('/test')
        assert response.status_code == 200
        assert response.data == b''  # Empty response body for OPTIONS


def test_load_user_api_key_present(test_app):
    """Test that a request with a valid API key proceeds."""
    with test_app.test_client() as client:
        response = client.get('/test', headers={"X-API-KEY": "valid_api_key"})
        assert response.status_code == 200
        assert response.json == {"message": "Success"}
        # Check if g.api_key is correctly set
        with test_app.test_request_context('/test', headers={"X-API-KEY": "valid_api_key"}):
            assert g.api_key == "valid_api_key"


def test_load_user_api_key_missing(test_app):
    """Test that a request without an API key returns a 401 error."""
    with test_app.test_client() as client:
        response = client.get('/test')
        assert response.status_code == 401
        assert response.json == {"error": "API key is required"}

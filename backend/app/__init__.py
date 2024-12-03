import os

from flask import Flask
from flask_cors import CORS

from .services.db_service import setup_db
from .utils.before_request import setup_before_request
from .utils.error_handler import setup_error_handlers


def create_app():
    app = Flask(__name__)

    CORS(
        app,
        resources={r"/*": {"origins": os.getenv('CORS_ORIGIN', 'http://localhost:5173')}},
        allow_headers='X-API-KEY'
    )

    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    setup_db(debug)

    from .routes.analyze import analyze_bp
    from .routes.query import query_bp
    from .routes.validate import validate_bp

    setup_before_request(app)

    app.register_blueprint(analyze_bp)
    app.register_blueprint(query_bp)
    app.register_blueprint(validate_bp)

    setup_error_handlers(app)

    return app

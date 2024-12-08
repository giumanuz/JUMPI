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
        allow_headers=[
            'Content-Type',
            'X-API-KEY',
            'Authorization',
            'Access-Control-Allow-Headers',
            'Access-Control-Allow-Origin'
        ],
    )

    setup_db()

    # from .routes.analyze import analyze_bp
    # from .routes.query import query_bp
    from .routes.validate import validate_bp
    from .routes.upload import upload_bp
    from .routes.info import info_bp
    # from .routes.edit import edit_bp

    setup_before_request(app)

    app.register_blueprint(upload_bp)
    # app.register_blueprint(analyze_bp)
    # app.register_blueprint(query_bp)
    app.register_blueprint(validate_bp)
    # app.register_blueprint(edit_bp)
    app.register_blueprint(info_bp)   

    setup_error_handlers(app)

    return app

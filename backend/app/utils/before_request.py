from flask import request, g


def setup_before_request(app):
    @app.before_request
    def load_user_api_key():
        if request.method == 'OPTIONS':
            return '', 200
        g.api_key = request.headers.get('X-API-KEY')
        if not g.api_key:
            return {"error": "API key is required"}, 401

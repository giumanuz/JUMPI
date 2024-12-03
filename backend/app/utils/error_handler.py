import logging

import elasticsearch


def setup_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_general_error(error):
        return {"error": str(error)}, 500

    @app.errorhandler(elasticsearch.ApiError)
    def handle_elasticsearch_api_error(error: elasticsearch.ApiError):
        logging.error("Elasticsearch error", exc_info=error)
        if error.status_code == 401:
            if error.message == "security_exception":
                return {"error": "Invalid API key"}, 401
            return {"error": "Unauthorized"}, 401
        if error.status_code // 100 == 4:
            return {"error": "Bad request"}, error.status_code
        if error.status_code // 100 == 5:
            logging.error("Database error", exc_info=error)
            return {"error": "Internal server error"}, error.status_code

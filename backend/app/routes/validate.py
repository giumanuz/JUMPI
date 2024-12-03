import logging

from flask import Blueprint
from werkzeug.exceptions import InternalServerError

from database_utils.database import Database

validate_bp = Blueprint('validate', __name__)


@validate_bp.route('/validate-api-key', methods=['GET'])
def validate_api_key():
    ping = Database.get_instance().ping()
    logging.error("Ping: %s", ping)
    if not ping:
        raise InternalServerError("Database is not available")
    return {"message": "API key is valid"}

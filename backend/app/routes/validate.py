import logging
from flask import Blueprint, jsonify
from app.services.database.database import Database

validate_bp = Blueprint('validate', __name__)

@validate_bp.route('/validate-api-key', methods=['GET'])
def validate_api_key():
    ping = Database.get_instance().ping()
    if not ping:
        return jsonify({"message": "Database is not available"}), 500
    return {"message": "API key is valid"}
import re

from flask import jsonify, request, Blueprint

from app.services.database.database import Database
from app.utils.converters import snake_to_camel_case

auth_bp = Blueprint('auth', __name__)


@auth_bp.errorhandler(TypeError)
# TODO: non so se questo sia utile per noi @edo
def handle_exception(e: TypeError):
    error_msg = e.args[0]
    matches = re.match(
        r".*? missing (\d+) required positional arguments: (.*)$", error_msg, flags=re.S)
    if not matches:
        return {'error': str(error_msg)}, 500
    num_missing_args = int(matches.group(1))
    missing_args = (matches.group(2)
                    .replace("and ", "")
                    .replace("'", "")
                    .split(", "))
    missing_args_camel = [snake_to_camel_case(arg) for arg in missing_args]
    return {'error': f"Missing {num_missing_args} required arguments: {', '.join(missing_args_camel)}"}, 400


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    is_present = Database.get_instance().exist_user(email)
    if not is_present:
        return jsonify({'error': 'User not found'}), 404
    is_logged = Database.get_instance().login_user(email, password)
    if not is_logged:
        return jsonify({'error': 'Wrong password'}), 401
    return jsonify({'message': 'Logged in'})


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    is_present = Database.get_instance().exist_user(email)
    if is_present:
        return jsonify({'error': 'User already exists'}), 409
    Database.get_instance().register_user(username, email, password)
    return jsonify({'message': 'User registered'})

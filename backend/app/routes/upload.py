import re

from flask import request, Blueprint

from app.services.database.database import Database
from app.utils.classes import Magazine, Article
from app.utils.parser import camel_to_snake_dict, snake_to_camel_case

upload_bp = Blueprint('upload', __name__)


@upload_bp.errorhandler(TypeError)
def handle_exception(e: TypeError):
    error_msg = e.args[0]
    matches = re.match(r".*? missing (\d+) required positional arguments: (.*)$", error_msg, flags=re.S)
    if not matches:
        return {'error': str(error_msg)}, 500
    num_missing_args = int(matches.group(1))
    missing_args = (matches.group(2)
                    .replace("and ", "")
                    .replace("'", "")
                    .split(", "))
    missing_args_camel = [snake_to_camel_case(arg) for arg in missing_args]
    return {'error': f"Missing {num_missing_args} required arguments: {', '.join(missing_args_camel)}"}, 400


@upload_bp.route('/uploadMagazine', methods=['POST'])
def upload_magazine():
    magazine_json: dict = camel_to_snake_dict(request.json)
    magazine = Magazine(**magazine_json)
    magazine_id = Database.get_instance().add_magazine(magazine)
    return {'id': magazine_id}


@upload_bp.route('/uploadArticle', methods=['POST'])
def upload_article():
    article_json: dict = camel_to_snake_dict(request.json)
    article = Article(**article_json)
    article_id = Database.get_instance().add_article(article)
    return {'id': article_id}


@upload_bp.route('/updateMagazine', methods=['POST'])
def update_magazine():
    magazine_json: dict = camel_to_snake_dict(request.json)
    magazine = Magazine.update_blueprint_with(**magazine_json)
    Database.get_instance().update_magazine(magazine)
    return "success"


@upload_bp.route('/updateArticle', methods=['POST'])
def update_article():
    article_json: dict = camel_to_snake_dict(request.json)
    article = Article.update_blueprint_with(**article_json)
    Database.get_instance().update_article(article)
    return "success"



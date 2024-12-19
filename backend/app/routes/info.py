from flask import Blueprint, request
from app.services.database.database import Database
from app.utils.parser import snake_to_camel, snake_to_camel_case
import re

info_bp = Blueprint('info', __name__)


@info_bp.before_request
def ensure_id_param():
    if request.method == 'GET' and 'id' not in request.args:
        return {'error': 'Missing required parameter: id'}, 400


@info_bp.errorhandler(TypeError)
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


@info_bp.route('/magazineInfo', methods=['GET'])
def info_documents():
    magazine_id = request.args.get('id')
    magazine = Database.get_instance().get_magazine(magazine_id)
    return snake_to_camel(magazine.to_dict())


@info_bp.route('/articleInfo', methods=['GET'])
def info_article():
    article_id = request.args.get('id')
    article = Database.get_instance().get_article(article_id)
    return snake_to_camel(article.to_dict())


@info_bp.route('/getArticlesFromMagazineid', methods=['GET'])
def get_articles_from_magazine():
    magazine_id = request.args.get('id')
    articles = Database.get_instance().get_articles_from_magazine(magazine_id)
    article_dicts = (article.to_dict() for article in articles)
    return {
        'articles': [snake_to_camel(d) for d in article_dicts]
    }

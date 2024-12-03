from flask import Blueprint, request

from app.utils.classes import Magazine, Article
from app.services.database.database import Database

query_bp = Blueprint('query', __name__)


@query_bp.route('/query', methods=['GET'])
def query_documents():
    query_params = request.args or {}

    # noinspection PyTypeChecker
    magazine = Magazine(
        name=query_params.get('name_magazine'),
        year=query_params.get('year'),
        publisher=query_params.get('publisher'),
        genre=query_params.get('genre'),
        abstract=None,
        articles=None
    )

    # noinspection PyTypeChecker
    article = Article(
        title=query_params.get('article_title'),
        author=query_params.get('article_author'),
        content=query_params.get('content'),
        images=None,
        page_offsets=None,
        page_range=None
    )

    return Database.get_instance().query(magazine, article)

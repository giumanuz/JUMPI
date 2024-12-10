from datetime import datetime
from flask import Blueprint, request

from app.utils.classes import Magazine, Article
from app.services.database.database import Database

query_bp = Blueprint('query', __name__)


@query_bp.route('/query', methods=['GET'])
def query_documents():
    query_params = request.args or {}

    magazine_date = datetime.strptime(query_params.get(
        'magazine_date'), "%Y-%m-%d") if query_params.get('magazine_date') else None
    genres = query_params.get('magazine_genre').split(
        ",") if query_params.get('magazine_genre') else None

    magazine = Magazine.query_blueprint_with(
        name=query_params.get('magazine_name'),
        date=magazine_date,
        publisher=query_params.get('magazine_publisher'),
        genres=genres,
    )

    article = Article.query_blueprint_with(
        title=query_params.get('article_title'),
        author=query_params.get('article_author'),
        content=query_params.get('article_content'),
    )

    return Database.get_instance().query(magazine, article)

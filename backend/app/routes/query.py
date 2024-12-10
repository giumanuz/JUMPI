from typing import Optional
from datetime import datetime
from flask import request, jsonify
from flask import Blueprint, request

from app.utils.classes import Magazine, Article
from app.services.database.database import Database

query_bp = Blueprint('query', __name__)


@query_bp.route('/query', methods=['GET'])
def query_documents():
    query_params = request.args or {}

    magazine = Magazine(
        id="",
        name=query_params.get('magazine_name', ""),
        date=datetime.strptime(query_params.get(
            'magazine_date', ""), "%Y-%m-%d") if query_params.get('magazine_date') else None,
        publisher=query_params.get('magazine_publisher', ""),
        edition=None,
        abstract=None,
        genres=query_params.get('magazine_genre', "").split(
            ",") if query_params.get('magazine_genre') else [],
        categories=[],
    )

    article = Article(
        id="",
        magazine_id="",
        title=query_params.get('article_title', ""),
        author=query_params.get('article_author', ""),
        page_range=[],
        page_scans=[],
        content=query_params.get('article_content', ""),
        page_offsets=[],
        figures=[],
    )

    return Database.get_instance().query(magazine, article)

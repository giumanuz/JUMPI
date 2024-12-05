from flask import Blueprint, request, jsonify
from app.utils.classes import Magazine, Article
from app.services.database.database import Database

edit_bp = Blueprint('edit', __name__)

@edit_bp.route('/edit', methods=['POST'])
def edit_documents():
    payload = request.json
    if not payload:
        return jsonify({"error": "Missing payload"}), 400

    magazine_data = payload.get("magazine")
    article_data = payload.get("article")

    if not magazine_data:
        return jsonify({"error": "Missing magazine data"}), 400

    magazine_id = magazine_data.get("id")
    magazine = Magazine(
        name=magazine_data.get("name"),
        year=magazine_data.get("year"),
        publisher=magazine_data.get("publisher"),
        genre=magazine_data.get("genre"),
    )

    article = None
    if article_data:
        article = Article(
            title=article_data.get("title"),
            author=article_data.get("author"),
            content=article_data.get("content"),
            page_range=article_data.get("page_range"),
            page_offsets=article_data.get("page_offsets"),
        )

    Database.get_instance().update_magazine(magazine_id, magazine)

    return jsonify({"message": "Document updated successfully"}), 200

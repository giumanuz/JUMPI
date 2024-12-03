import json

from flask import Blueprint, request

from app.services.database.database import Database
from app.services.file_processor import process_files
from app.utils.classes import Magazine, Article

analyze_bp = Blueprint('analyze', __name__)


@analyze_bp.route('/analyze-documents', methods=['POST'])
def analyze_documents():
    if 'files' not in request.files:
        return {"error": "No files provided"}, 400

    files = request.files.getlist('files')
    if not files:
        return {"error": "No files selected"}, 400

    metadata = request.form.get('metadata')
    if not metadata:
        return {"error": "Missing metadata"}, 400

    try:
        metadata = json.loads(metadata)
    except json.JSONDecodeError:
        return {"error": "Invalid metadata format"}, 400

    required_fields = ["name_magazine", "year", "publisher", "genre", "article_title", "article_author",
                       "article_page_range"]
    for field in required_fields:
        if field not in metadata:
            return {"error": f"Missing required field: {field}"}, 400

    combined_text, offsets, image_base64_list = process_files(files)

    magazine = Magazine(
        name=metadata["name_magazine"],
        year=metadata["year"],
        publisher=metadata["publisher"],
        genre=metadata["genre"],
    )

    page_range = metadata["article_page_range"]
    page_range = [int(r) for r in page_range.split("-")]

    article = Article(
        title=metadata["article_title"],
        author=metadata["article_author"],
        content=combined_text,
        page_range=page_range,
        page_offsets=offsets
    )

    Database.get_instance().add_article(magazine, article)

    return {
        "extracted_text": combined_text,
        "image_comparisons": image_base64_list
    }

import base64
import json
import logging
import re

from flask import jsonify, request, Blueprint

from app.services.database.database import Database
from app.services.file_processor import process_files
from app.utils.classes import Magazine, Article, ArticlePageScan
from app.utils.parser import camel_to_snake, snake_to_camel_case, snake_to_camel

upload_bp = Blueprint('upload', __name__)


@upload_bp.errorhandler(TypeError)
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


@upload_bp.route('/uploadMagazine', methods=['POST'])
def upload_magazine():
    magazine_json: dict = camel_to_snake(request.json)
    magazine = Magazine.create_blueprint_with(**magazine_json)
    magazine_id = Database.get_instance().add_magazine(magazine)
    return {'id': magazine_id}


@upload_bp.route('/getMagazines', methods=['GET'])
def get_magazines():
    magazines = Database.get_instance().get_all_magazines()
    magazine_dicts = (magazine.to_dict() for magazine in magazines)
    return {
        'magazines': [snake_to_camel(d) for d in magazine_dicts]
    }


@upload_bp.route('/uploadArticle', methods=['POST'])
def upload_article_and_return_results():
    # TODO: remove this, just for testing
    # with open('output.json', 'r') as f:
    #     return jsonify(json.loads(f.read()))
    # return
    form_data = camel_to_snake(request.form.to_dict())
    form_data['page_range'] = json.loads(form_data.get('page_range'))
    files = request.files
    scans_file_storages = files.getlist("scans")
    page_scans = []
    for i, scan_fs in enumerate(scans_file_storages):
        image_data = scan_fs.read()
        scan_fs.stream.seek(0)
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        page_scans.append(ArticlePageScan(i + 1, image_base64))

    process_result = process_files(scans_file_storages)

    for scan_fs in scans_file_storages:
        scan_fs.close()

    return snake_to_camel({
        'text': process_result.text,
        'scan_results': [
            {
                'page': i + 1,
                'comparison_image': image_data
            } for i, image_data in enumerate(process_result.comparison_base64_images)
        ],
        'figures': [
            {
                'page': figure.page,
                'caption': figure.caption,
                'image_data': figure.image_data,
            } for figure in process_result.figures
        ],
        'page_scans': [
            {
                'page': page_scan.page,
                'image_data': page_scan.image_data,
                'uploaded_on': page_scan.uploaded_on.isoformat()
            } for page_scan in page_scans
        ]
    })

# TODO: Da rivedere la logica di salvataggio dell'articolo
@upload_bp.route('/saveEditedArticle', methods=['POST'])
def save_edited_article():
    article_json = camel_to_snake(request.json)
    body_str = article_json.get('body')

    if not body_str:
        return {"error": "Missing 'body' in request"}, 400

    try:
        body = camel_to_snake(json.loads(body_str))
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON in 'body': {str(e)}"}, 400

    try:
        article_without_figures = Article.create_blueprint_with(
            **{k: v for k, v in body.items() if k != 'figures'}
        )

        logging.error("prima richiesta")
        article_id = Database.get_instance().add_article(article_without_figures)
        logging.error(f"article_id: {article_id}")

        article = Database.get_instance().get_article(article_id)
        article.figures = body.get('figures', [])

        logging.error("seconda richiesta")
        Database.get_instance().update_article(article)

        return {"id": article_id}, 200
    except Exception as e:
        logging.error(f"Error processing article: {e}")
        return {"error": "Internal server error"}, 500


@upload_bp.route('/updateMagazine', methods=['POST'])
def update_magazine():
    magazine_json: dict = camel_to_snake(request.json)
    magazine = Magazine.update_blueprint_with(**magazine_json)
    Database.get_instance().update_magazine(magazine)
    return "success"


@upload_bp.route('/updateArticle', methods=['PUT'])
def update_article():
    updated_data = request.json
    article_id = updated_data.get("id")

    existing_article = Database.get_instance().get_article(article_id)
    if not existing_article:
        return jsonify({"error": "Article not found"}), 404

    existing_article.title = updated_data.get("title", existing_article.title)
    existing_article.author = updated_data.get(
        "author", existing_article.author)
    existing_article.page_range = updated_data.get(
        "page_range", existing_article.page_range)
    existing_article.content = updated_data.get(
        "content", existing_article.content)

    Database.get_instance().update_article(existing_article)
    return jsonify({"success": True})

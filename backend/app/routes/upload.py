import base64
import json
import logging
import re

from flask import jsonify, request, Blueprint

from app.services.database.database import Database
from app.services.file_processor import process_files
from app.utils.classes import Magazine, Article, ArticlePageScan
from app.utils.parser import camel_to_snake_dict, snake_to_camel_case, snake_to_camel_dict

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
    magazine_json: dict = camel_to_snake_dict(request.json)
    magazine = Magazine.create_blueprint_with(**magazine_json)
    magazine_id = Database.get_instance().add_magazine(magazine)
    return {'id': magazine_id}


@upload_bp.route('/getMagazines', methods=['GET'])
def get_magazines():
    magazines = Database.get_instance().get_all_magazines()
    magazine_dicts = (magazine.to_dict() for magazine in magazines)
    return {
        'magazines': [snake_to_camel_dict(d) for d in magazine_dicts]
    }


@upload_bp.route('/uploadArticle', methods=['POST'])
def upload_article_and_return_results():
    form_data = request.form.to_dict()
    form_data['pageRange'] = json.loads(form_data.get('pageRange'))
    files = request.files
    article_json = camel_to_snake_dict(form_data)
    scans_file_storages = files.getlist("scans")
    page_scans = []
    for i, scan_fs in enumerate(scans_file_storages):
        image_data = scan_fs.read()
        scan_fs.stream.seek(0)
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        page_scans.append(ArticlePageScan(i + 1, image_base64))

    process_result = process_files(scans_file_storages)
    article = Article.create_blueprint_with(
        content=process_result.text,
        page_offsets=process_result.page_offsets,
        page_scans=page_scans,
        **article_json
    )
    article_id = Database.get_instance().add_article(article)

    for scan_fs in scans_file_storages:
        scan_fs.close()

    return {
        'articleId': article_id,
        'text': process_result.text,
        'scanResults': [
            {
                'page': i + 1,
                'comparisonImage': image_data
            } for i, image_data in enumerate(process_result.comparison_base64_images)
        ]}


@upload_bp.route('/updateMagazine', methods=['POST'])
def update_magazine():
    magazine_json: dict = camel_to_snake_dict(request.json)
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
    existing_article.author = updated_data.get("author", existing_article.author)
    existing_article.page_range = updated_data.get("page_range", existing_article.page_range)
    existing_article.content = updated_data.get("content", existing_article.content)
    
    Database.get_instance().update_article(existing_article)
    return jsonify({"success": True})


import base64
import logging
import re

from flask import request, Blueprint

from app.services.database.database import Database
from app.utils.classes import Magazine, Article, ArticlePageScan
from app.utils.parser import camel_to_snake_dict, snake_to_camel_case, snake_to_camel_dict

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
    form_data = request.form
    files = request.files
    article_json = camel_to_snake_dict(form_data)
    scans_file_storages = files.getlist("scans")
    page_scans = []
    for i, scan_fs in enumerate(scans_file_storages):
        image_data = scan_fs.read()
        scan_fs.close()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        page_scans.append(ArticlePageScan(i + 1, image_base64))

    article = Article.create_blueprint_with(page_scans=page_scans, **article_json)
    # article_id = Database.get_instance().add_article(article)
    article_id = "123"
    logging.error(f"Article ID: {article_id}")
    logging.error(f"Article: {article}")
    # TODO: Return the extracted text and image comparisons
    return {
        'articleId': article_id,
        'scanResults': [
            {
                'page': i+1,
                'text': "This is a sample text extracted from the scan.",
                'comparisonImage': "iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAABx0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4xLjEsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy+AADFEAAAgAElEQVR4nOzdeXwUZf7/8e9z7z"
            } for i in range(len(article.page_scans))
        ]}


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

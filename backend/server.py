import base64
import concurrent.futures
import json
import logging
import os
import shutil
from pathlib import Path
from threading import Lock

import elasticsearch
from aws.call_api import analyze_document as aws_analyze_document
from azure.call_api import analyze_document as azure_analyze_document
from dotenv import load_dotenv
from flask import Flask, request, g
from flask_cors import CORS
from werkzeug.exceptions import InternalServerError
from werkzeug.utils import secure_filename

from database_utils.classes import Article, Magazine
from database_utils.database import Database
from database_utils.elastic import ElasticsearchDb
from main import process_file

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": os.getenv('CORS_ORIGIN', 'http://localhost:5173')}}, allow_headers='X-API-KEY')

file_processing_lock = Lock()

TEMP_FOLDER = './temp'
IMAGE_FOLDER = './temp/images'
IMAGE_COMPARISON_FOLDER = './temp/images_comparison'
AWS_FOLDER = './temp/aws'
AZURE_FOLDER = './temp/azure'
REPORT_FOLDER = './temp/reports'
GPT_FOLDER = './temp/gpt'

Path(IMAGE_FOLDER).mkdir(parents=True, exist_ok=True)
Path(IMAGE_COMPARISON_FOLDER).mkdir(parents=True, exist_ok=True)
Path(AWS_FOLDER).mkdir(parents=True, exist_ok=True)
Path(AZURE_FOLDER).mkdir(parents=True, exist_ok=True)
Path(REPORT_FOLDER).mkdir(parents=True, exist_ok=True)
Path(GPT_FOLDER).mkdir(parents=True, exist_ok=True)


def process_single_file(file):
    filename = secure_filename(file.filename)
    file_path = Path(IMAGE_FOLDER) / filename
    file.save(file_path)
    aws_analyze_document(file_path, AWS_FOLDER)
    azure_analyze_document(file_path, AZURE_FOLDER)
    json_file = Path(filename).with_suffix('.json').name
    process_file(json_file, AZURE_FOLDER, AWS_FOLDER, GPT_FOLDER, REPORT_FOLDER, IMAGE_FOLDER, IMAGE_COMPARISON_FOLDER,
                 file_path)
    return filename


@app.before_request
def load_user_api_key():
    if request.method == 'OPTIONS':
        return '', 200
    g.api_key = request.headers.get('X-API-KEY')
    if not g.api_key:
        return {"error": "API key is required"}, 401


# Error handling
@app.errorhandler(elasticsearch.ApiError)
def handle_elasticsearch_api_error(error: elasticsearch.ApiError):
    logging.error("Elasticsearch error", exc_info=error)
    logging.error(g.api_key)
    if error.status_code == 401:
        if error.message == "security_exception":
            return {"error": "Invalid API key"}, 401
        return {"error": "Unauthorized"}, 401
    if error.status_code // 100 == 4:
        return {"error": "Bad request"}, error.status_code
    if error.status_code // 100 == 5:
        logging.error("Database error", exc_info=error)
        return {"error": "Internal server error"}, error.status_code

@app.route('/validate-api-key', methods=['GET'])
def validate_api_key():
    ping = Database.get_instance().ping()
    logging.error("Ping: %s", ping)
    if not ping:
        raise InternalServerError("Database is not available")
    return {"message": "API key is valid"}


@app.route('/analyze-documents', methods=['POST'])
def analyze_documents_endpoint():
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

    with file_processing_lock:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            filenames = executor.map(process_single_file, files)

        combined_text = []
        response_text = []
        offsets = []
        for text_file in Path(GPT_FOLDER).iterdir():
            if not text_file.is_file():
                continue
            with text_file.open('r') as f:
                content = f.read()
            offsets.append(len(content) + (offsets[-1] if offsets else 0))
            combined_text.append(content)
            content = f"{text_file.name:-^50}\n" + content + f"\n{'-' * 50}\n"
            response_text.append(content)

        image_base64_list = []
        image_paths = [os.path.join(IMAGE_COMPARISON_FOLDER, filename) for filename in filenames]
        for image_path in image_paths:
            with Path(image_path).open('rb') as image_file:
                image_data = image_file.read()
                image_base64_list.append(base64.b64encode(image_data).decode('utf-8'))

        temp_folder = Path(TEMP_FOLDER)
        if temp_folder.exists() and temp_folder.is_dir():
            shutil.rmtree(temp_folder)
            temp_folder.mkdir()

    print("\n".join(combined_text))

    extracted_text = "\n".join(combined_text)

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
        content=extracted_text,
        page_range=page_range,
        page_offsets=offsets
    )

    res = Database.get_instance().add_article(magazine, article)
    print(res)

    return {
        "extracted_text": "\n".join(response_text),
        "image_comparisons": image_base64_list
    }


@app.route('/query', methods=['GET'])
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


def setup_db(debug=False):
    elastic_url = os.getenv('ELASTIC_URL')
    db = ElasticsearchDb(url=elastic_url)
    db.logger.setLevel(logging.DEBUG if debug else logging.INFO)
    Database.set_instance(db)


if __name__ == '__main__':
    load_dotenv()
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5123))
    setup_db(debug=debug)
    app.run(debug=debug, host=host, port=port)

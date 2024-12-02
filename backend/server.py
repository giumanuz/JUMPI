import logging
import shutil
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import concurrent.futures
from pathlib import Path
import json
import os
import base64
from flask_cors import CORS

from database_utils.classes import Article, Magazine
from database_utils.database import Database
from database_utils.elastic import ElasticsearchDb
from main import process_file
from werkzeug.utils import secure_filename
from aws.call_api import analyze_document as aws_analyze_document
from azure.call_api import analyze_document as azure_analyze_document
from threading import Lock


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": os.getenv('CORS_ORIGIN', 'http://localhost:5173')}})

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
    process_file(json_file, AZURE_FOLDER, AWS_FOLDER, GPT_FOLDER, REPORT_FOLDER, IMAGE_FOLDER, IMAGE_COMPARISON_FOLDER, file_path)
    return filename

@app.route('/analyze-documents', methods=['POST'])
def analyze_documents_endpoint():
    if request.method == 'OPTIONS':
        return '', 200

    if 'files' not in request.files:
        return jsonify({"error": "No files provided"}), 400
    
    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No files selected"}), 400

    metadata = request.form.get('metadata')
    if not metadata:
        return jsonify({"error": "Missing metadata"}), 400

    try:
        metadata = json.loads(metadata)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid metadata format"}), 400

    required_fields = ["name_magazine", "year", "publisher", "genre", "article_title", "article_author", "article_page_range"]
    for field in required_fields:
        if field not in metadata:
            return jsonify({"error": f"Missing required field: {field}"}), 400

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
            content = f"{text_file.name:-^50}\n" + content + f"\n{'-'*50}\n"
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

    response = {
        "extracted_text": "\n".join(response_text),
        "image_comparisons": image_base64_list
    }

    return jsonify(response)

@app.route('/query', methods=['GET'])
def query_documents():
    query_params = request.args or {}

    magazine = Magazine(
        name=query_params.get('name_magazine'),
        year=query_params.get('year'),
        publisher=query_params.get('publisher'),
        genre=query_params.get('genre'),
        abstract=None,
        articles=None
    )

    article = Article(
        title=query_params.get('article_title'),
        author=query_params.get('article_author'),
        content=query_params.get('content'),
        images=None,
        page_offsets=None,
        page_range=None
    )

    res = Database.get_instance().query(magazine, article)

    return jsonify(res)


def setup_db():
    elastic_url = os.getenv('ELASTIC_URL')
    elastic_api_key = os.getenv('ELASTIC_API_KEY')
    db = ElasticsearchDb(url=elastic_url, api_key=elastic_api_key)
    Database.set_instance(db)
    info = db.connect()
    logging.info(info)
    if not db.is_connected():
        raise Exception("Could not connect to the database")

if __name__ == '__main__':
    load_dotenv()
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5123))
    setup_db()
    app.run(debug=debug, host=host, port=port)

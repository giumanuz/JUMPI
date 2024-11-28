from flask import Flask, request, jsonify
import concurrent.futures
from pathlib import Path
import json
import os
from flask_cors import CORS

from main import process_file
from werkzeug.utils import secure_filename
from aws.call_api import analyze_document as aws_analyze_document
from azure.call_api import analyze_document as azure_analyze_document


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


TEMP_FOLDER = './temp'
IMAGE_FOLDER = './temp/images'
IMAGE_COMPARISON_FOLDER = './temp/images_comparison'
AWS_FOLDER = './temp/aws'
AZURE_FOLDER = './temp/azure'
REPORT_FOLDER = './temp/reports'
GPT_FOLDER = './temp/gpt'

os.makedirs(TEMP_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(IMAGE_COMPARISON_FOLDER, exist_ok=True)
os.makedirs(AWS_FOLDER, exist_ok=True)
os.makedirs(AZURE_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)
os.makedirs(GPT_FOLDER, exist_ok=True)


def process_single_file(file):
    filename = secure_filename(file.filename)
    file_path = os.path.join(IMAGE_FOLDER, filename)
    file.save(file_path)
    aws_analyze_document(file_path, AWS_FOLDER)
    azure_analyze_document(file_path, AZURE_FOLDER)
    json_file = Path(filename).with_suffix('.json').name
    process_file(json_file, AZURE_FOLDER, AWS_FOLDER, GPT_FOLDER, REPORT_FOLDER, IMAGE_FOLDER, IMAGE_COMPARISON_FOLDER, file_path)

@app.route('/analyze-documents', methods=['POST'])
def analyze_documents_endpoint():
    if request.method == 'OPTIONS':
        # Rispondere alla richiesta preflight con status 200
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

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_single_file, files)

    combined_text = ''
    for text_file in [f for f in os.listdir(GPT_FOLDER)]:
        with open(os.path.join(GPT_FOLDER, text_file), 'r') as f:
            combined_text += f.read() + '\n\n'

    response = {
        "extracted_text": combined_text,
        "image_caption_pairs": [],
    }

    # TODO: Save the extracted text and image-caption pairs to the database

    return jsonify(response)

@app.route('/query', methods=['POST'])
def query_documents():
    query_params = request.json or {}
    results = []

    # TODO: perform query on the database

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5123)

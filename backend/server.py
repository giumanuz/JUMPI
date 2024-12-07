# mock_server.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid
import logging

app = Flask(__name__)
CORS(app)  # Abilita CORS per tutte le rotte

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# In-memory data storage
magazines = {}
articles = {}

# Sample Data
def initialize_data():
    mag_id = str(uuid.uuid4())
    magazines[mag_id] = {
        "id": mag_id,
        "name": "Tech Today",
        "date": datetime.now().isoformat(),
        "publisher": "Tech Publishers Inc.",
        "edition": "Spring 2024",
        "abstract": "A magazine covering the latest in technology.",
        "genres": ["Technology", "Science"],
        "categories": ["Gadgets", "AI"],
        "created_on": datetime.now().isoformat(),
        "edited_on": datetime.now().isoformat(),
    }

    art_id = str(uuid.uuid4())
    articles[art_id] = {
        "id": art_id,
        "magazine_id": mag_id,
        "title": "The Rise of AI",
        "author": "Jane Doe",
        "page_range": [10, 15],
        "content": "Content of the article goes here.",
        "page_offsets": [0, 0],  # Placeholder
        "figures": [],  # Placeholder
        "created_on": datetime.now().isoformat(),
        "edited_on": datetime.now().isoformat(),
    }

initialize_data()

# Helper Functions
def validate_api_key(api_key):
    # For mock purposes, accept any non-empty key
    return bool(api_key)

# Routes

## API Key Validation
@app.route("/validate-api-key", methods=["GET"])
def validate_api_key_route():
    api_key = request.headers.get("X-API-KEY")
    if validate_api_key(api_key):
        return jsonify({"status": "valid"}), 200
    else:
        return jsonify({"status": "invalid"}), 401

## Magazines

@app.route("/getMagazines", methods=["GET"])
def get_magazines():
    return jsonify({"magazines": list(magazines.values())}), 200

@app.route("/magazines/<mag_id>", methods=["GET"])
def get_magazine(mag_id):
    magazine = magazines.get(mag_id)
    if magazine:
        return jsonify({"magazine": magazine}), 200
    else:
        return jsonify({"error": "Magazine not found"}), 404

@app.route("/magazines", methods=["POST"])
def add_magazine():
    data = request.json
    mag_id = str(uuid.uuid4())
    new_magazine = {
        "id": mag_id,
        "name": data.get("name"),
        "date": data.get("date"),
        "publisher": data.get("publisher"),
        "edition": data.get("edition"),
        "abstract": data.get("abstract"),
        "genres": data.get("genres", []),
        "categories": data.get("categories", []),
        "created_on": datetime.now().isoformat(),
        "edited_on": datetime.now().isoformat(),
    }
    magazines[mag_id] = new_magazine
    return jsonify({"magazine": new_magazine}), 201

@app.route("/magazines/<mag_id>", methods=["PUT"])
def update_magazine(mag_id):
    if mag_id not in magazines:
        return jsonify({"error": "Magazine not found"}), 404

    data = request.json
    magazine = magazines[mag_id]

    # Update fields
    magazine["name"] = data.get("name", magazine["name"])
    magazine["date"] = data.get("date", magazine["date"])
    magazine["publisher"] = data.get("publisher", magazine["publisher"])
    magazine["edition"] = data.get("edition", magazine.get("edition"))
    magazine["abstract"] = data.get("abstract", magazine.get("abstract"))
    magazine["genres"] = data.get("genres", magazine["genres"])
    magazine["categories"] = data.get("categories", magazine["categories"])
    magazine["edited_on"] = datetime.now().isoformat()

    magazines[mag_id] = magazine
    return jsonify({"magazine": magazine}), 200

## Article

@app.route("/articles/<art_id>", methods=["GET"])
def get_article(art_id):
    logging.error(f"tutti gli articoli: {articles}")
    logging.error(f"Getting article with ID: {art_id}")
    article = articles.get(art_id)
    if article:
        return jsonify({"article": article}), 200
    else:
        return jsonify({"error": "Article not found"}), 404

@app.route("/articles", methods=["POST"])
def add_article():
    data = request.json
    art_id = str(uuid.uuid4())
    new_article = {
        "id": art_id,
        "magazine_id": data.get("magazine_id"),
        "title": data.get("title"),
        "author": data.get("author"),
        "page_range": data.get("page_range", []),
        "content": data.get("content", ""),
        "page_offsets": data.get("page_offsets", []),
        "figures": data.get("figures", []),
        "created_on": datetime.now().isoformat(),
        "edited_on": datetime.now().isoformat(),
    }
    articles[art_id] = new_article
    return jsonify({"article": new_article}), 201

@app.route("/articles/<art_id>", methods=["PUT"])
def update_article(art_id):
    logging.error((f"tutti gli articoli: {articles}"))
    logging.error(f"Updating article with ID: {art_id}")
    if art_id not in articles:
        return jsonify({"error": "Article not found"}), 404

    data = request.json
    article = articles[art_id]

    # Update fields
    article["title"] = data.get("title", article["title"])
    article["author"] = data.get("author", article["author"])
    page_range = data.get("page_range")
    if page_range:
        article["page_range"] = page_range
    article["content"] = data.get("content", article["content"])
    # Aggiorna altri campi se necessario
    article["edited_on"] = datetime.now().isoformat()

    articles[art_id] = article
    return jsonify({"article": article}), 200

## Upload Article (Mock Endpoint)
@app.route("/uploadArticle", methods=["POST"])
def upload_article():
    # Implementazione mock
    data = request.form
    files = request.files.getlist("images")
    title = data.get("title")
    author = data.get("author")
    page_range = data.get("pageRange")
    magazine_id = data.get("magazineId")

    # Crea un nuovo articolo
    art_id = str(uuid.uuid4())
    new_article = {
        "id": art_id,
        "magazine_id": magazine_id,
        "title": title,
        "author": author,
        "page_range": [int(x) for x in page_range.split("-")],
        "content": "Extracted content from images.",  # Contenuto mock
        "page_offsets": [0, 0],  # Placeholder
        "figures": [],  # Placeholder
        "created_on": datetime.now().isoformat(),
        "edited_on": datetime.now().isoformat(),
    }

    articles[art_id] = new_article

    # Risposta mock
    return jsonify({
        "status": "ok",
        "article": {
            "extracted_text": new_article["content"],
            "image_comparisons": []  # Placeholder
        }
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=5123)

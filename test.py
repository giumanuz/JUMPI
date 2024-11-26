import pytest
import json
from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_analyze_documents(client):
    metadata = json.dumps({
        "name_magazine": "Magazine Name",
        "abstract_magazine": "Abstract",
        "year": 2023,
        "publisher": "Publisher Name",
        "genre": "Science",
        "articles": [
            {"title": "Article 1", "author": "Author 1", "page_range": "1-10"},
            {"title": "Article 2", "author": "Author 2", "page_range": "11-20"}
        ]
    })

    with open('images/7.jpg', 'rb') as file1, open('images/8.jpg', 'rb') as file2:
        response = client.post(
            '/analyze-documents',
            data={
                'metadata': metadata,
                'files': [file1, file2]
            },
            content_type='multipart/form-data'
        )
        print(response.json)

    assert response.status_code == 200
    assert "extracted_text" in response.json
    assert "image_caption_pairs" in response.json
    assert len(response.json["extracted_text"]) != 0

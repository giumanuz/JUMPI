import pytest
import json
from pathlib import Path
from aws.extract_lines import extract_lines 

@pytest.fixture
def mock_textract_json(tmp_path):
    """Fixture to create a mock Textract JSON response."""
    mock_data = {
        "Blocks": [
            {"BlockType": "LINE", "Text": "First line of text"},
            {"BlockType": "WORD", "Text": "Word not included"},
            {"BlockType": "LINE", "Text": "Second line of text"},
        ]
    }
    json_file = tmp_path / "mock_textract.json"
    json_file.write_text(json.dumps(mock_data))
    return str(json_file)


def test_extract_lines(mock_textract_json):
    """Test the extract_lines function to ensure it extracts only lines of text."""
    lines = extract_lines(mock_textract_json)
    assert lines == ["First line of text", "Second line of text"]

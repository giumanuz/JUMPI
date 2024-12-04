import pytest
from unittest.mock import MagicMock
from azure.extract_lines import (
    compute_overlap_percentage,
    is_line_inside_figure,
    gpt_is_caption,
    is_line_in_captions,
    get_confidence,
    extract_lines,
)
from commons import Polygon, Line
import json


@pytest.fixture
def mock_data(tmp_path):
    """Fixture to create a mock JSON input for testing."""
    mock_json = {
        "figures": [
            {
                "boundingRegions": [{"polygon": [1, 1, 4, 1, 4, 4, 1, 4]}],
                "caption": {
                    "spans": [{"offset": 5, "length": 10}],
                },
            }
        ],
        "paragraphs": [
            {"role": "pageNumber", "spans": [{"offset": 15}]},
            {"content": "This is a test paragraph", "spans": [{"offset": 30, "length": 25}]},
        ],
        "pages": [
            {
                "lines": [
                    {
                        "content": "Line 1 content",
                        "polygon": [2, 2, 3, 2, 3, 3, 2, 3],
                        "spans": [{"offset": 35, "length": 15}],
                    },
                    {
                        "content": "Line 2 content",
                        "polygon": [4, 4, 6, 4, 6, 6, 4, 6],
                        "spans": [{"offset": 45, "length": 15}],
                    },
                ],
                "words": [
                    {"span": {"offset": 35, "length": 15}, "confidence": 0.95},
                    {"span": {"offset": 45, "length": 15}, "confidence": 0.9},
                ],
            }
        ],
    }
    mock_file = tmp_path / "mock_data.json"
    mock_file.write_text(json.dumps(mock_json))
    return str(mock_file)


def test_compute_overlap_percentage():
    """Test compute_overlap_percentage function."""
    polygon1 = Polygon([1, 1, 4, 1, 4, 4, 1, 4])
    polygon2 = Polygon([2, 2, 3, 2, 3, 3, 2, 3])

    polygon1.to_shapely = MagicMock()
    polygon2.to_shapely = MagicMock()
    polygon1.to_shapely.return_value.intersection.return_value.area = 1.0
    polygon1.to_shapely.return_value.area = 4.0
    polygon2.to_shapely.return_value.area = 1.0

    result = compute_overlap_percentage(polygon1, polygon2)
    assert result == 0.25


def test_is_line_inside_figure():
    """Test is_line_inside_figure function."""
    line_polygon = Polygon([2, 2, 3, 2, 3, 3, 2, 3])
    figure_polygon = Polygon([1, 1, 4, 1, 4, 4, 1, 4])

    compute_overlap_percentage_mock = MagicMock(return_value=1.0)
    result = is_line_inside_figure(line_polygon, [figure_polygon], threshold=0.5)
    assert result


def test_gpt_is_caption():
    """Test gpt_is_caption function."""
    assert not gpt_is_caption("Test paragraph")


def test_is_line_in_captions():
    """Test is_line_in_captions function."""
    line_spans = [{"offset": 10, "length": 5}]
    caption_spans = [(8, 10)]
    result = is_line_in_captions(line_spans, caption_spans)
    assert result


def test_get_confidence():
    """Test get_confidence function."""
    line_spans = [{"offset": 10, "length": 5}]
    words = [{"span": {"offset": 10, "length": 5}, "confidence": 0.8}]
    result = get_confidence(line_spans, words)
    assert result == 0.8


def test_extract_lines(mock_data):
    """Test extract_lines function."""
    lines = extract_lines(mock_data)
    assert len(lines) == 1
    assert lines[0].content == "Line 2 content"
    assert lines[0].confidence == 0.9

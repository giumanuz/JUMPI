import pytest
from unittest.mock import MagicMock, mock_open, patch
from app.services.ocr_readers.azure_reader import AzureDiReader
from commons import Polygon
import json
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def mock_azure_client(mocker):
    """Fixture to mock Azure Document Intelligence client."""
    mock_client = MagicMock()
    mocker.patch("app.services.ocr_readers.azure_reader.DocumentIntelligenceClient", return_value=mock_client)
    return mock_client


@pytest.fixture
def azure_di_reader(mock_azure_client, tmp_path):
    """Fixture to create an instance of AzureDiReader."""
    image_path = tmp_path / "test_image.png"
    image_path.write_bytes(b"fake_image_data")
    return AzureDiReader(image_path=str(image_path))


def test_read_to_file(azure_di_reader, mock_azure_client, tmp_path):
    """Test the read_to_file method to ensure results are saved correctly."""
    mock_result = MagicMock()
    mock_result.as_dict.return_value = {"blocks": [{"type": "line", "text": "Test line"}]}
    mock_azure_client.begin_analyze_document.return_value.result.return_value = mock_result

    output_dir = tmp_path
    azure_di_reader.read_to_file(output_dir=str(output_dir))
    output_file = tmp_path / azure_di_reader.json_result_filename

    assert output_file.exists()
    with open(output_file, "r") as file:
        data = json.load(file)
        assert data == {"blocks": [{"type": "line", "text": "Test line"}]}


def test_get_lines(azure_di_reader, tmp_path):
    """Test the get_lines method to extract lines of text from the JSON file."""
    json_result_file = tmp_path / azure_di_reader.json_result_filename
    json_result_file.write_text(json.dumps({
        "pages": [{
            "lines": [
                {
                    "content": "Sample text",
                    "polygon": [1, 1, 2, 2, 3, 3, 4, 4],
                    "spans": [{"offset": 0, "length": 11}]
                }
            ],
            "words": [{"span": {"offset": 0, "length": 11}, "confidence": 0.99}]
        }]
    }))
    azure_di_reader.json_result_filename = str(json_result_file)

    azure_di_reader.image_path = str(json_result_file)
    lines = azure_di_reader.get_lines()

    assert len(lines) == 1
    assert lines[0].content == "Sample text"
    assert lines[0].confidence == 0.99


def test_analyze_document(azure_di_reader, mock_azure_client):
    """Test the __analyze_document method to ensure it calls Azure API correctly."""
    mock_result = MagicMock()
    mock_azure_client.begin_analyze_document.return_value.result.return_value = mock_result

    with patch("builtins.open", mock_open(read_data=b"fake_image_data")) as mocked_file:
        response = azure_di_reader._AzureDiReader__analyze_document()

        mock_azure_client.begin_analyze_document.assert_called_once_with(
            "prebuilt-layout",
            analyze_request=mocked_file.return_value,
            content_type="application/octet-stream"
        )
        assert response == mock_result


def test_save_result_to_file(azure_di_reader, tmp_path):
    """Test the __save_result_to_file method to save analysis results to a JSON file."""
    mock_result = MagicMock()
    mock_result.as_dict.return_value = {"blocks": [{"type": "line", "text": "Test line"}]}
    output_file = tmp_path / "output.json"

    azure_di_reader._AzureDiReader__save_result_to_file(mock_result, output_file)

    assert output_file.exists()
    with open(output_file, "r") as f:
        data = json.load(f)
        assert data == {"blocks": [{"type": "line", "text": "Test line"}]}


def test_is_line_inside_figure(azure_di_reader):
    """Test the __is_line_inside_figure method to detect if a line is inside a figure."""
    polygon1 = Polygon([1, 1, 4, 1, 4, 4, 1, 4])
    polygon2 = Polygon([2, 2, 3, 2, 3, 3, 2, 3])

    mock_polygon1 = MagicMock()
    mock_polygon1.intersection.return_value.area = 1.0
    mock_polygon1.area = 2.0

    mock_polygon2 = MagicMock()
    mock_polygon2.area = 1.0

    with patch.object(Polygon, "to_shapely", side_effect=[mock_polygon1, mock_polygon2]):
        azure_di_reader._AzureDiReader__figure_polygons.append(polygon2)
        is_inside = azure_di_reader._AzureDiReader__is_line_inside_figure(polygon1, threshold=0.5)

    assert is_inside


def test_is_line_in_captions(azure_di_reader):
    """Test the __is_line_in_captions method to detect if a line is in captions."""
    azure_di_reader._AzureDiReader__caption_spans.append((0, 11))
    line_spans = [{"offset": 5, "length": 5}]

    is_in_caption = azure_di_reader._AzureDiReader__is_line_in_captions(line_spans)
    assert is_in_caption

import pytest
from unittest.mock import MagicMock, patch
from app.services.ocr_readers.aws_reader import AwsTextractReader
import json

@pytest.fixture
def mock_boto3_client(mocker):
    """Fixture to mock the boto3 client."""
    mock_textract = MagicMock()
    mocker.patch("boto3.client", return_value=mock_textract)
    return mock_textract


@pytest.fixture
def aws_textract_reader(mock_boto3_client, tmp_path):
    """Fixture to create an instance of AwsTextractReader."""
    image_path = tmp_path / "test_image.png"
    image_path.write_bytes(b"fake_image_data")
    return AwsTextractReader(image_path=str(image_path))


def test_read_to_file(aws_textract_reader, mock_boto3_client, tmp_path):
    """Test the read_to_file method to ensure results are saved correctly."""
    mock_boto3_client.analyze_document.return_value = {"Blocks": [{"BlockType": "LINE", "Text": "Test line"}]}
    output_dir = tmp_path
    aws_textract_reader.read_to_file(output_dir=str(output_dir))
    output_file = tmp_path / aws_textract_reader.json_result_filename

    assert output_file.exists()
    with open(output_file, 'r') as file:
        data = json.load(file)
        assert data == {"Blocks": [{"BlockType": "LINE", "Text": "Test line"}]}


def test_get_lines(aws_textract_reader, tmp_path):
    """Test the get_lines method to retrieve text lines from the JSON file."""
    json_result_file = tmp_path / aws_textract_reader.json_result_filename
    json_result_file.write_text(json.dumps({"Blocks": [{"BlockType": "LINE", "Text": "Sample text"}]}))
    aws_textract_reader.json_result_filename = str(json_result_file)

    lines = aws_textract_reader.get_lines()
    assert lines == ["Sample text"]


def test_analyze_document(aws_textract_reader, mock_boto3_client):
    """Test the __analyze_document method to ensure it calls Textract correctly."""
    mock_boto3_client.analyze_document.return_value = {"MockKey": "MockValue"}
    image_bytes = b"fake_image_data"
    response = aws_textract_reader._AwsTextractReader__analyze_document(image_bytes)

    mock_boto3_client.analyze_document.assert_called_once_with(
        Document={"Bytes": image_bytes},
        FeatureTypes=["LAYOUT"]
    )
    assert response == {"MockKey": "MockValue"}


def test_save_result_to_file(aws_textract_reader, tmp_path):
    """Test the __save_result_to_file method to save results to a JSON file."""
    response = {"TestKey": "TestValue"}
    output_file = tmp_path / "output.json"
    aws_textract_reader._AwsTextractReader__save_result_to_file(response, output_file)

    assert output_file.exists()
    with open(output_file, 'r') as f:
        data = json.load(f)
        assert data == response

from base64 import b64encode
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Lock

from werkzeug.utils import secure_filename

from app.config import Config
from app.services.ocr_readers.aws_reader import AwsTextractReader
from app.services.ocr_readers.azure_reader import AzureDiReader
from app.utils.matching_utils import process_file

file_processing_lock = Lock()


def process_files(files):
    with file_processing_lock:
        with ThreadPoolExecutor() as executor:
            filenames = executor.map(_process_file, files)

        combined_text = []
        offsets = []
        for text_file in Path(Config.GPT_FOLDER).iterdir():
            if not text_file.is_file():
                continue
            with text_file.open('r') as f:
                content = f.read()
            offsets.append(len(content) + (offsets[-1] if offsets else 0))
            combined_text.append(content)

        image_base64_list = []
        image_paths = [Path(Config.IMAGE_COMPARISON_FOLDER) / filename for filename in filenames]
        for image_path in image_paths:
            with Path(image_path).open('rb') as image_file:
                image_data = image_file.read()
                image_base64_list.append(b64encode(image_data).decode('utf-8'))

        Config.flush_temp_dirs()

    combined_text = "\n".join(combined_text)
    return combined_text, offsets, image_base64_list


def _process_file(file):
    filename = secure_filename(file.filename)
    file_path = Path(Config.IMAGE_FOLDER) / filename
    file.save(file_path)
    AwsTextractReader(file_path).read_to_file(Config.AWS_FOLDER)
    AzureDiReader(file_path).read_to_file(Config.AZURE_FOLDER)

    json_file = Path(filename).with_suffix('.json').name
    process_file(json_file, str(file_path))
    return filename

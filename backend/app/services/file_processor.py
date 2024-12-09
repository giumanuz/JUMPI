import logging
from base64 import b64encode
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Iterator

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.config import Config
from app.services.ocr_readers.aws_reader import AwsTextractReader
from app.services.ocr_readers.azure_reader import AzureDiReader
from app.utils.matching_utils import process_file

file_processing_lock = Lock()


@dataclass
class ProcessResult:
    text: str
    page_offsets: list[int]
    comparison_base64_images: list[str]


def process_files(files: list[FileStorage]) -> ProcessResult:
    with file_processing_lock:
        filenames = _process_files_and_get_filenames(files)
        combined_text, offsets = _get_text_and_page_offsets()
        comparison_images_b64 = _get_base64_comparison_images(filenames)
        # Config.flush_temp_dirs()

    return ProcessResult(combined_text, offsets, comparison_images_b64)


def _get_base64_comparison_images(filenames):
    image_base64_list = []
    image_paths = [Path(Config.IMAGE_COMPARISON_FOLDER) / filename for filename in filenames]
    for image_path in image_paths:
        with Path(image_path).open('rb') as image_file:
            image_data = image_file.read()
            image_base64_list.append(b64encode(image_data).decode('utf-8'))
    return image_base64_list


def _get_text_and_page_offsets() -> tuple[str, list[int]]:
    pages_contents = []
    page_offsets = []
    for text_file in Path(Config.GPT_FOLDER).iterdir():
        if not text_file.is_file():
            continue
        with text_file.open('r') as f:
            content = f.read()
        page_offsets.append(len(content) + (page_offsets[-1] if page_offsets else 0))
        pages_contents.append(content)
    pages_contents = "\n".join(pages_contents)
    return pages_contents, page_offsets


def _process_files_and_get_filenames(files: list[FileStorage]) -> Iterator[str]:
    with ThreadPoolExecutor() as executor:
        return executor.map(_process_file_and_get_filename, files)


def _process_file_and_get_filename(file: FileStorage):
    file_path = _save_file_on_disk_and_get_path(file)

    AwsTextractReader(file_path).read_to_file(Config.AWS_FOLDER)
    AzureDiReader(file_path).read_to_file(Config.AZURE_FOLDER)

    json_filename = file_path.with_suffix('.json').name
    process_file(json_filename, str(file_path))
    return file_path.name


def _save_file_on_disk_and_get_path(file: FileStorage) -> Path:
    filename = secure_filename(file.filename)
    file_path = Path(Config.IMAGE_FOLDER) / filename
    logging.error(f"FILE ---- {file.stream.read()}")
    file.save(file_path)
    return file_path


def _read_lines(file_path: Path) -> list[str]:
    with open(file_path, 'r') as file:
        return file.readlines()

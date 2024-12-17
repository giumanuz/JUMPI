from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from threading import Lock
from typing import Iterator
import logging

from werkzeug.datastructures import FileStorage

from app.utils.matching_utils import _process_file
from app.utils.classes import ResultComparison, ProcessResult

file_processing_lock = Lock()


def process_files(files: list[FileStorage]) -> ProcessResult:
    with file_processing_lock:
        results = _process_files(files)
        combined_text = _get_text(results)
        comparison_images_b64 = [elem.comparison_image for elem in results]
        figures = [elem.figures for elem in results]

    return ProcessResult(combined_text, comparison_images_b64, figures)


def _get_text(results: list[ResultComparison]) -> str:
    pages_contents = []
    for result in results:
        pages_contents.append(
            result.gpt_lines if result.gpt_lines else result.azure_lines)

    return '\n'.join(pages_contents)


def _process_files(files: list[FileStorage]) -> Iterator[ResultComparison]:
    with ThreadPoolExecutor() as executor:
        return list(executor.map(_process_file, files))
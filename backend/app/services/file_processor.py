from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from werkzeug.datastructures import FileStorage

from app.utils.matching_utils import _process_file
from app.utils.classes import ResultComparison, ProcessResult

file_processing_lock = Lock()


def process_files(files: list[FileStorage]) -> ProcessResult:
    with file_processing_lock:
        results: list[ResultComparison] = _process_files(files)
        combined_text = "\n".join([elem.user_text for elem in results])
        comparison_images_b64 = [elem.comparison_image for elem in results]
        figures = [figure for elem in results for figure in elem.figures]

    return ProcessResult(combined_text, comparison_images_b64, figures)


def _process_files(files: list[FileStorage]) -> list[ResultComparison]:
    with ThreadPoolExecutor() as executor:
        return list(executor.map(_process_file, files))

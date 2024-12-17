import base64
import logging
from functools import cache
from typing import Optional
from io import BytesIO

import openai
from Levenshtein import ratio
from PIL import ImageDraw

from app.services.openai_client import OpenaiClient
from commons import MatchedLine, LINE_NOT_FOUND
from app.services.ocr_readers.aws_reader import AwsTextractReader
from app.services.ocr_readers.azure_reader import AzureDiReader
from app.utils.classes import ResultComparison
from werkzeug.datastructures import FileStorage


__openai_client: Optional[OpenaiClient] = None

logger = logging.getLogger(__name__)


def _process_file(
        file: FileStorage,
        threshold_high=0.95,
        threshold_low=0.90,
) -> ResultComparison:

    aws_reader = AwsTextractReader(file)
    azure_reader = AzureDiReader(file)
    aws_reader.load_json()
    azure_reader.load_json()

    azure_lines = azure_reader.get_lines()
    aws_strings = aws_reader.get_lines()

    matched_lines = [MatchedLine(azure_line) for azure_line in azure_lines]

    _match(matched_lines, aws_strings)

    azure_lines_content = ""
    aws_lines_content = ""
    for matched_line in matched_lines:
        azure_lines_content += matched_line.azure_line.content + "\n"
        aws_lines_content += (
            matched_line.aws_string if matched_line.aws_string else LINE_NOT_FOUND) + "\n"

    prompt = f"AZURE:\n{azure_lines_content}\n--------------\nAWS:\n{aws_lines_content}"
    gpt_ans = _get_gpt_merged_text(prompt)

    gpt_strings = gpt_ans.split("\n")
    _match(matched_lines, gpt_strings, is_gpt=True)

    return _generate_result_comparison(
        azure_reader,
        matched_lines,
        threshold_high,
        threshold_low,
    )


def _get_openai_client():
    global __openai_client
    if __openai_client is None:
        __openai_client = OpenaiClient(
            system_prompt=_get_correction_system_prompt(),
            max_tokens=16384,
            temperature=0.2,
            model="gpt-4o"
        )
    return __openai_client


@cache
def _get_correction_system_prompt() -> str:
    with open("gpt_prompts/two-tools.md", "r") as f:
        return f.read()


def _get_gpt_merged_text(user_prompt: str) -> str:
    try:
        content = _get_openai_client().get_completion(user_prompt)
        return _strip_all_lines(content)
    except openai.OpenAIError as e:
        logger.error(f"Error in API request", exc_info=e)
        return ""


def _strip_all_lines(text: str) -> str:
    return "\n".join((l.strip() for l in text.split("\n")))


def _match(matched_lines: list[MatchedLine], strings_to_match: list[str], is_gpt: bool = False, threshold: float = 0.8):
    import heapq

    # Set to store the indexes of the strings_to_match that have already been matched
    selected_lines = set()
    # Heap of (-similarity, azure_idx, idx_to_match). Heap is a min heap, so we negate similarity to get better matches first
    heap = []
    for idx_to_match, string_to_match in enumerate(strings_to_match):
        for azure_idx, matched_line in enumerate(matched_lines):
            similarity = ratio(
                matched_line.azure_line.content, string_to_match)
            if similarity >= threshold:
                heapq.heappush(heap, (-similarity, azure_idx, idx_to_match))

    while len(heap) > 0:
        _, azure_idx, idx_to_match = heapq.heappop(heap)

        # Azure line already matched
        if is_gpt and matched_lines[azure_idx].gpt_string:
            continue
        if not is_gpt and matched_lines[azure_idx].aws_string:
            continue

        # String to match already matched
        if idx_to_match in selected_lines:
            continue

        selected_lines.add(idx_to_match)
        if is_gpt:
            matched_lines[azure_idx].gpt_string = strings_to_match[idx_to_match]
        else:
            matched_lines[azure_idx].aws_string = strings_to_match[idx_to_match]


def _generate_result_comparison(
        azure_reader: AzureDiReader,
        matched_lines: list[MatchedLine],
        threshold_high,
        threshold_low,
) -> ResultComparison:
    azure_strings = []
    aws_strings = []
    gpt_strings = []
    user_text = []

    image_highlighted = azure_reader.image
    draw = ImageDraw.Draw(image_highlighted, 'RGBA')

    for idx, matched_line in enumerate(matched_lines):
        polygon = matched_line.azure_line.polygons[0]
        similarity = matched_line.get_similarity()
        if similarity < threshold_low:
            _draw_polygon(draw, polygon, 'red')
        elif similarity < threshold_high:
            _draw_polygon(draw, polygon, 'yellow')

        azure_strings.append(matched_line.azure_line.content)
        aws_strings.append(matched_line.aws_string)
        gpt_strings.append(matched_line.gpt_string)
        user_text.append(
            matched_line.gpt_string if matched_line.gpt_string else matched_line.azure_line.content)

    buffered = BytesIO()
    image_highlighted.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    figures = azure_reader.get_figures()

    return ResultComparison(
        azure_lines=azure_strings,
        aws_lines=aws_strings,
        gpt_lines=gpt_strings,
        comparison_image=img_base64,
        user_text="\n".join(user_text),
        figures=figures,
    )


def _draw_polygon(draw, polygon, color):
    colors = {
        'yellow': (255, 230, 0, 40),
        'red': (255, 0, 0, 40)
    }
    polygon_points = [(point.x, point.y) for point in polygon.points]
    draw.polygon(polygon_points, outline=color, width=0, fill=colors[color])

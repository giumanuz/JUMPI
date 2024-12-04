import os
import re
from Levenshtein import ratio
from functools import cache

import openai
from PIL import Image, ImageDraw
from dotenv import load_dotenv

from app.config import Config
from aws.extract_lines import extract_lines as extract_lines_aws
from azure.extract_lines import extract_lines as extract_lines_azure
from commons import MatchedLine, LINE_NOT_FOUND

load_dotenv()

client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))


@cache
def _get_correction_system_prompt() -> str:
    with open("gpt_prompts/two-tools.md", "r") as f:
        return f.read()


def _call_api(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": _get_correction_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            max_tokens=16384,
            temperature=0.2
        )
        content = response.choices[0].message.content
        all_lines = "\n".join((l.strip() for l in content.split("\n")))
        match = re.search(r"AZURE:\s*(.*?)(?=\s*AWS:|\s*-{2,})", all_lines, re.DOTALL)

        return match.group(1) if match else all_lines
    except Exception as e:
        print(f"Error in API request: {e}")
        return ""


def _match(matched_lines: list[MatchedLine], strings_to_match: list[str], is_gpt: bool=False, threshold: float=0.8):
    import heapq

    # Set to store the indexes of the strings_to_match that have already been matched
    selected_lines = set()
    # Heap of (-similarity, azure_idx, idx_to_match). Heap is a min heap, so we negate similarity to get better matches first
    heap = []
    for idx_to_match, string_to_match in enumerate(strings_to_match):
        for azure_idx, matched_line in enumerate(matched_lines):
            similarity = ratio(matched_line.azure_line.content, string_to_match)
            if similarity >= threshold:
                heapq.heappush(heap, (-similarity, azure_idx, idx_to_match))
    
    while heap:
        similarity, azure_idx, idx_to_match = heapq.heappop(heap)
        similarity = -similarity

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


def process_file(
        filename: str,
        image_path: str,
        threshold_high=95,
        threshold_low=90,
):
    azure_file_path = os.path.join(Config.AZURE_FOLDER, filename)
    aws_file_path = os.path.join(Config.AWS_FOLDER, filename)

    if not (os.path.isfile(azure_file_path) and os.path.isfile(aws_file_path)):
        return

    azure_lines = extract_lines_azure(azure_file_path)
    aws_strings = extract_lines_aws(aws_file_path)

    matched_lines = [MatchedLine(azure_line) for azure_line in azure_lines]

    _match(matched_lines, aws_strings)

    azure_lines_content = ""
    aws_lines_content = ""
    for matched_line in matched_lines:
        azure_lines_content += matched_line.azure_line.content + "\n"
        aws_lines_content += (matched_line.aws_string if matched_line.aws_string else LINE_NOT_FOUND) + "\n"

    prompt = f"AZURE:\n{azure_lines_content}\n--------------\nAWS:\n{aws_lines_content}"
    gpt_ans = _call_api(prompt)

    output_path = os.path.join(Config.GPT_FOLDER, filename).replace('.json', '.txt')
    with open(output_path, 'w') as f:
        f.write(gpt_ans)

    gpt_strings = gpt_ans.split("\n")
    _match(matched_lines, gpt_strings, is_gpt=True)

    _create_output_and_visuals(
        filename,
        matched_lines,
        image_path,
        threshold_high,
        threshold_low,
    )


def _create_output_and_visuals(
        azure_file: str,
        matched_lines: list[MatchedLine],
        image_path: str,
        threshold_high=95,
        threshold_low=90,
):
    comparison_image_path = os.path.join(Config.IMAGE_COMPARISON_FOLDER, os.path.basename(image_path))
    output_file_path = os.path.join(Config.REPORT_FOLDER, f'{azure_file}.txt').replace('.json', '')

    with open(output_file_path, 'w') as output_file:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            draw = ImageDraw.Draw(img, 'RGBA')
            for idx, matched_line in enumerate(matched_lines):
                polygon = matched_line.azure_line.polygons[0] # See why [0] in the definition of Line class
                similarity = matched_line.get_similarity()
                if similarity < threshold_low:
                    _draw_polygon(draw, polygon, 'red')
                elif similarity < threshold_high:
                    _draw_polygon(draw, polygon, 'yellow')
                
                output_file.write(f"Azure: {matched_line.azure_line.content}\n")
                output_file.write(f"AWS:   {matched_line.aws_string if matched_line.aws_string else LINE_NOT_FOUND}\n")
                output_file.write(f"GPT:   {matched_line.gpt_string if matched_line.gpt_string else LINE_NOT_FOUND}\n")
                output_file.write("\n" + "-"*50 + "\n\n")
                
            img.save(comparison_image_path)


def _draw_polygon(draw, polygon, color):
    colors = {
        'yellow': (255, 230, 0, 40),
        'red': (255, 0, 0, 40)
    }
    polygon_points = [(point.x, point.y) for point in polygon.points]
    draw.polygon(polygon_points, outline=color, width=0, fill=colors[color])

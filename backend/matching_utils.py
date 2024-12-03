import os
import re
from difflib import SequenceMatcher
from functools import cache
from typing import Tuple, List

import openai
from PIL import Image, ImageDraw
from dotenv import load_dotenv
from tqdm import tqdm

from aws.extract_lines import extract_lines as extract_lines_aws
from azure.extract_lines import extract_lines as extract_lines_azure
from commons import Line

load_dotenv()

client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))


@cache
def get_correction_system_prompt() -> str:
    with open("gpt_prompts/two-tools.md", "r") as f:
        return f.read()


def call_api(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": get_correction_system_prompt()},
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


def custom_matcher(source_line_content: str, target_lines: set[str], threshold=80):
    best_match = None
    best_score = 0

    for target_line in target_lines:
        score = SequenceMatcher(None, source_line_content, target_line).ratio() * 100

        if score > best_score and score >= threshold:
            best_match = target_line
            best_score = score

    return (best_match, best_score) if best_match else None


def fuzzy_match_lines(
        matched_pairs: List[Tuple[Line, str, float]],
        source_lines: List[Line],
        target_lines: set[str],
        threshold=80
):
    for idx, source_line in enumerate(source_lines):
        best_match = custom_matcher(source_line.content, target_lines, threshold)
        if best_match:
            matched_pairs[idx] = (source_line, best_match[0], best_match[1])
            target_lines.remove(best_match[0])
        elif matched_pairs[idx] is None:
            matched_pairs[idx] = (source_line, '<Line not found>', 0)
    return matched_pairs


def iterative_fuzzy_matching(
        source_lines: List[Line],
        target_lines: List[str],
        initial_threshold=100,
        penalty_step=1,
        max_threshold=50
) -> List[Tuple[Line, str, float]]:
    matches: List[Tuple[Line, str, float]] = [None] * len(source_lines)
    set_target_lines = set(target_lines)
    threshold = initial_threshold

    while threshold >= max_threshold:
        matches = fuzzy_match_lines(matches, source_lines, set_target_lines, threshold=threshold)
        threshold -= penalty_step

    return matches


def process_file(
        azure_file: str,
        azure_dir: str,
        aws_dir: str,
        output_dir_merged_gpt_lines: str,
        output_dir: str,
        images_dir_input: str,
        images_out_input: str,
        image_path: str,
        threshold_high=95,
        threshold_low=90,
):
    azure_file_path = os.path.join(azure_dir, azure_file)
    aws_file_path = os.path.join(aws_dir, azure_file)

    if not (os.path.isfile(azure_file_path) and os.path.isfile(aws_file_path)):
        return

    azure_lines = extract_lines_azure(azure_file_path)
    aws_lines = extract_lines_aws(aws_file_path)

    matches_azure_aws = iterative_fuzzy_matching(azure_lines, aws_lines)
    azure_lines_content = "\n".join([line.content for line, _, _ in matches_azure_aws])
    aws_lines_content = "\n".join([line for _, line, _ in matches_azure_aws])

    prompt = f"AZURE:\n{azure_lines_content}\n--------------\nAWS:\n{aws_lines_content}"
    corrected_lines = call_api(prompt)

    output_path = os.path.join(output_dir_merged_gpt_lines, azure_file).replace('.json', '.txt')
    with open(output_path, 'w') as f:
        f.write(corrected_lines)

    gpt_lines = corrected_lines.split("\n")
    matches_azure_gpt = iterative_fuzzy_matching(azure_lines, gpt_lines)

    create_output_and_visuals(
        azure_file,
        matches_azure_aws,
        matches_azure_gpt,
        images_dir_input,
        images_out_input,
        output_dir,
        image_path,
        threshold_high,
        threshold_low,
    )


def create_output_and_visuals(
        azure_file: str,
        matches_azure_aws: List[Tuple[Line, str, float]],
        matches_azure_gpt: List[Tuple[Line, str, float]],
        images_dir_input: str,
        images_out_input: str,
        output_dir: str,
        image_path: str,
        threshold_high=95,
        threshold_low=90,
):
    comparison_image_path = os.path.join(images_out_input, os.path.basename(image_path))
    output_file_path = os.path.join(output_dir, f'{azure_file}.txt').replace('.json', '')

    with open(output_file_path, 'w') as output_file:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            draw = ImageDraw.Draw(img, 'RGBA')
            for idx, (azure, aws, score) in enumerate(matches_azure_aws):
                polygon = azure.polygons[0]
                gpt_line = matches_azure_gpt[idx][1]
                if score < threshold_low:
                    draw_polygon(draw, polygon, 'red')
                elif score < threshold_high:
                    draw_polygon(draw, polygon, 'yellow')
                output_file.write(f"{azure.content} \n{aws}\n{gpt_line}\n\n\n")
            img.save(comparison_image_path)


def draw_polygon(draw, polygon, color):
    colors = {
        'yellow': (255, 230, 0, 40),
        'red': (255, 0, 0, 40)
    }
    polygon_points = [(point.x, point.y) for point in polygon.points]
    draw.polygon(polygon_points, outline=color, width=0, fill=colors[color])


def main(
        azure_dir='azure/json',
        aws_dir='aws/json',
        output_dir='compare-aws-azure-gpt',
        output_dir_merged_gpt_lines='gpt/lines',
        images_dir_input='images',
        images_out_input='images-comparison',
        threshold_high=95,
        threshold_low=90,
):
    ensure_directories([output_dir, output_dir_merged_gpt_lines, images_out_input])
    for azure_file in tqdm(os.listdir(azure_dir)):
        print(f'Processing {azure_file}')
        process_file(
            azure_file,
            azure_dir,
            aws_dir,
            output_dir_merged_gpt_lines,
            output_dir,
            images_dir_input,
            images_out_input,
            threshold_high,
            threshold_low,
        )


def ensure_directories(directories: List[str]):
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

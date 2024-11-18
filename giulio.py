import os
from difflib import SequenceMatcher
from functools import cache

from PIL import Image, ImageDraw
from typing import Tuple

from commons import Line
from aws.extract_lines import extract_lines as extract_lines_aws
from azure.extract_lines import extract_lines as extract_lines_azure
from dotenv import load_dotenv
import openai
from tqdm import tqdm

load_dotenv()

client = openai.Client(api_key=os.getenv("OPENAI_API_KEY")) 

@cache
def get_correction_system_prompt() -> str:
    with open("gpt_prompt_together.md", "r") as f:
        return f.read()
    
def call_api(prompt):
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
        return "\n".join((l.strip() for l in content.split("\n")))
    except Exception as e:
        print(f"Error in API request: {e}")
        return None


def custom_matcher(source_line_content, target_lines, threshold=80):
    best_match = None
    best_score = 0

    for target_line in target_lines:
        target_line_content = target_line.content
        score = SequenceMatcher(None, source_line_content, target_line_content).ratio() * 100

        if score > best_score and score >= threshold:
            best_match = target_line
            best_score = score

    return (best_match, best_score) if best_match else None


def fuzzy_match_lines(matched_pairs, source_lines: list[Line], target_lines: set[Line], threshold=80):
    for idx, source_line in enumerate(source_lines):
        best_match = custom_matcher(source_line.content, target_lines, threshold)

        if best_match:
            matched_pairs[idx] = (source_line, best_match[0], best_match[1])
            target_lines.remove(best_match[0])
        elif matched_pairs[idx] is None:
            matched_pairs[idx] = (source_line, Line([], '<Line not found>', 0, []), 0)

    return matched_pairs


# questa funzione ritorna una lista di Tuple[Line_source, Line_target, score]
def iterative_fuzzy_matching(source_lines, target_lines, initial_threshold=100, penalty_step=1, max_threshold=50) -> list[Tuple[Line, Line, float]]:
    matches: list[Line] = [None] * len(source_lines)
    set_target_lines = set(target_lines)
    threshold = initial_threshold

    while threshold >= max_threshold:
        matches = fuzzy_match_lines(matches, source_lines, set_target_lines, threshold=threshold)

        threshold -= penalty_step

    return matches


azure_dir = 'azure-json'
aws_dir = 'aws-json'
output_dir = 'compare-lines2'
output_dir_merged_gpt_lines = 'merged-gpt-lines'
images_dir_input = 'Images'
images_out_input = 'Images-comparison'
THREASHOLD_HIGH = 95
THREASHOLD_MEDIUM = 90
THREASHOLD_LOW = 85

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

if not os.path.exists(images_out_input):
    os.makedirs(images_out_input)

if not os.path.exists(output_dir_merged_gpt_lines):
    os.makedirs(output_dir_merged_gpt_lines)

for azure_file in tqdm(os.listdir(azure_dir)):
    print(f'Processing {azure_file}')
    azure_file_path = os.path.join(azure_dir, azure_file)
    aws_file_path = os.path.join(aws_dir, azure_file)

    if os.path.isfile(azure_file_path) and os.path.isfile(aws_file_path):
        azure_lines = extract_lines_azure(azure_file_path)
        aws_lines = extract_lines_aws(aws_file_path)

        matches_azure_aws = iterative_fuzzy_matching(azure_lines, aws_lines)

        lines_1 = "\n".join([line.content for line, _, _ in matches_azure_aws])
        lines_2 = "\n".join([line.content for _, line, _ in matches_azure_aws])

        prompt = f"AZURE:\n{lines_1}\n--------------\nAWS:\n{lines_2}"
        corrected_lines = call_api(prompt)

        # TODO: change the names of the output files because now it is .json
        with open(os.path.join(output_dir_merged_gpt_lines, azure_file), 'w') as f:
            f.write(corrected_lines)

        gpt_lines = [Line([], line, 0, []) for line in corrected_lines.split("\n")]

        matches_azure_gpt = iterative_fuzzy_matching(azure_lines, gpt_lines)

        image_path = os.path.join(images_dir_input, azure_file.replace('.json', '.JPG'))
        comparison_image_path = os.path.join(images_out_input, azure_file.replace('.json', '.JPG'))
        output_file_path = os.path.join(output_dir, f'{azure_file}_report.txt').replace('.json', '')

        with open(output_file_path, 'w') as output_file:
            with Image.open(image_path) as img:
                img = img.convert("RGB")
                draw = ImageDraw.Draw(img, 'RGBA')
                for idx, (source, target, score) in enumerate(matches_azure_aws):
                    polygon = source.polygons[0]
                    if score >= THREASHOLD_HIGH:
                        output_file.write(f"{source.content}\n\n")
                    elif score >= THREASHOLD_MEDIUM:
                        gpt_line = matches_azure_gpt[idx][1]
                        polygon_points = [(point.x, point.y) for point in polygon.points]
                        draw.polygon(polygon_points, outline='yellow', width=0, fill=(255, 230, 0, 40))
                        output_file.write(f"{source.content} \n{target.content}\n{gpt_line.content}\n{score:.1f}%\n\n")
                    else:
                        gpt_line = matches_azure_gpt[idx][1]
                        polygon_points = [(point.x, point.y) for point in polygon.points]
                        draw.polygon(polygon_points, outline='red', width=0, fill=(255, 0, 0, 40))
                        output_file.write(f"{source.content} \n{target.content}\n{gpt_line.content}\n{score:.1f}%\n\n")

                img.save(comparison_image_path)

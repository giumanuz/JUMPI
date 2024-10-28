from rapidfuzz import fuzz, process
import pandas as pd
import os
from extract_lines_aws import extract_lines as extract_lines_aws
from extract_lines_azure import extract_lines as extract_lines_azure
from commons import Line
from PIL import Image, ImageDraw

def fuzzy_match_lines(matched_pairs, source_lines: list[Line], target_lines, threshold=80) : 
    
    for idx, source_line in enumerate(source_lines):
        best_match = process.extractOne(source_line.content, target_lines, scorer=fuzz.ratio, score_cutoff=threshold)

        if best_match:
            matched_pairs[idx] = (source_line, best_match[0], best_match[1])
            target_lines.remove(best_match[0]) 
        elif matched_pairs[idx] is None:
            matched_pairs[idx] = (source_line, '<Line not found>', 0)
    
    return matched_pairs

def iterative_fuzzy_matching(source_lines, target_lines_content, initial_threshold=100, penalty_step=1, max_threshold=50):
    matches : list[Line] = [None] * len(source_lines)
    threshold = initial_threshold
    

    while threshold >= max_threshold:
        matches = fuzzy_match_lines(matches, source_lines, target_lines_content, threshold=threshold)
        
        threshold -= penalty_step
    
    return matches

azure_dir = 'azure-json'
aws_dir = 'aws-json'
output_dir = 'compare-lines'
images_dir_input = 'Images'
images_out_input = 'Images-comparison'
THREASHOLD_HIGH = 95
THREASHOLD_MEDIUM = 90
THREASHOLD_LOW = 85

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

if not os.path.exists(images_out_input):
    os.makedirs(images_out_input)


for azure_file in os.listdir(azure_dir):
    azure_file_path = os.path.join(azure_dir, azure_file)
    aws_file_path = os.path.join(aws_dir, azure_file)

    
    if os.path.isfile(azure_file_path) and os.path.isfile(aws_file_path):
        file1_lines = extract_lines_azure(azure_file_path)
        file2_lines = extract_lines_aws(aws_file_path)

        target_lines_content = [line.content for line in file2_lines]

        
        matches = iterative_fuzzy_matching(file1_lines, target_lines_content)

        image_path = os.path.join(images_dir_input, azure_file.replace('.json', '.JPG'))
        comparison_image_path = os.path.join(images_out_input, azure_file.replace('.json', '.JPG'))
        output_file_path = os.path.join(output_dir, f'{azure_file}_report.txt')

        with open(output_file_path, 'w') as output_file:
            with Image.open(image_path) as img:
                img = img.convert("RGB")
                draw = ImageDraw.Draw(img, 'RGBA')
                for source, target, score in matches:
                    polygon = source.polygons[0]
                    if score>=THREASHOLD_HIGH:
                        output_file.write(f"{source.content}\n\n")
                    elif score>=THREASHOLD_MEDIUM:
                        polygon_points = [(point.x, point.y) for point in polygon.points]
                        draw.polygon(polygon_points, outline='yellow', width=0, fill=(255, 230, 0, 40))
                        output_file.write(f"{source.content} \n{target}\n{score:.1f}%\n\n")
                    else:
                        polygon_points = [(point.x, point.y) for point in polygon.points]
                        draw.polygon(polygon_points, outline='red', width=0, fill=(255, 0, 0, 40))
                        output_file.write(f"{source.content} \n{target}\n{score:.1f}%\n\n")
                    
                img.save(comparison_image_path)


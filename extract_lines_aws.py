import json
from commons import Polygon, Line, is_line_inside_figure, gpt_correct_line, gpt_is_caption
import os

def get_data(filename: str):
    # Open and load the JSON file
    with open(filename, "r") as f:
        data = json.load(f)['Blocks']
    
    # Extract text blocks and lines
    text_blocks = [doc for doc in data if doc['BlockType'] == 'LAYOUT_TEXT' or doc['BlockType'] == 'LAYOUT_TITLE' or doc['BlockType'] == 'LAYOUT_SECTION_HEADER' or doc['BlockType'] == 'LAYOUT_HEADER']
    lines = {doc["Id"]: (doc["Text"], doc["Confidence"], doc["Geometry"]["Polygon"]) for doc in data if doc['BlockType'] == 'LINE'}
    
    # Initialize whole text
    whole_text = ""
    paragraphs = []
    for block in text_blocks:
        paragraph_text = ""
        paragraph_children_id = []
        children = [r for r in block.get('Relationships', []) if r['Type'] == 'CHILD']
        for child in children:
            for id in child['Ids']:
                line = lines.get(id, "")[0]
                # if line.endswith("-"):
                #     line = line[:-1]
                # else:
                #     line += " "   EDO FAI TE 
                whole_text += line
                paragraph_text += line
                paragraph_children_id.append(id)
        paragraphs.append((paragraph_text.strip(), paragraph_children_id))
        whole_text += "\n"
    
    return (whole_text, paragraphs, lines)

def extract_lines(file_path: str) -> list[Line]:
    whole_text, paragraphs, lines = get_data(file_path)
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    figuresPolygons = []
    lines_result = []
    for block in data['Blocks']:
        if block.get('BlockType') == 'LAYOUT_FIGURE':
            points = []
            for point in block['Geometry']['Polygon']:
                points.append(point['X'])
                points.append(point['Y'])
            figuresPolygons.append(Polygon(points))
    
    for paragraph in paragraphs:
        if not gpt_is_caption(whole_text, paragraph[0]):
            for id in paragraph[1]:
                line = lines.get(id, "")
                points = []
                for point in line[2]:
                    points.append(point['X'])
                    points.append(point['Y'])
                line_polygon = Polygon(points)
                if is_line_inside_figure(line_polygon, figuresPolygons):
                    continue
                line_content = gpt_correct_line(whole_text, line[0])
                line_confidence = line[1]
                line_polygons = [line_polygon]
                lines_result.append(Line(polygons=line_polygons, content=line_content, confidence=line_confidence))

    return lines_result

if __name__ == "__main__":
    input_folder = "aws-json"
    output_folder = "aws-lines"
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            input_path = os.path.join(input_folder, filename)
            lines = extract_lines(input_path)
            
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_path, "w") as output_file:
                for line in lines:
                    output_file.write(line.content + "\n")
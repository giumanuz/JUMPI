import json, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from commons import Polygon, Line, is_line_inside_figure, gpt_is_caption

def get_data(data: list[dict]) -> tuple[list[tuple[str, list[str]], dict]]:
    # lines is a dictionary {line_id: (text, confidence, polygon)}
    lines = {doc["Id"]: [doc["Text"], doc["Confidence"], doc["Geometry"]["Polygon"]] for doc in data if doc['BlockType'] == 'LINE'}

    # blocks to extract paragraphs
    blocks_type = {'LAYOUT_TITLE', 'LAYOUT_HEADER', 'LAYOUT_FOOTER', 'LAYOUT_SECTION_HEADER', 'LAYOUT_LIST', 'LAYOUT_TEXT', 'LAYOUT_FIGURE'}
    text_blocks = [doc for doc in data if doc['BlockType'] in blocks_type]

    # paragraphs is a list(tuple(paragraph_text, list(children_id)))
    paragraphs = []
    for block in text_blocks:
        paragraph_text = ""
        children_id = []
        children = [r for r in block.get('Relationships', []) if r['Type'] == 'CHILD']
        for child in children:
            for id in child['Ids']:
                if id not in lines.keys():
                    continue
                line_text = lines.get(id, "")[0]
                paragraph_text += line_text
                children_id.append(id)
                if block['BlockType'] == 'LAYOUT_FIGURE':
                    lines[id].append(True)
        # if paragraph_text is not empty
        if paragraph_text:
            paragraphs.append((paragraph_text.strip(), children_id))
    
    return (paragraphs, lines)

def extract_lines(file_path: str) -> list[Line]:
    with open(file_path, 'r') as file:
        data = json.load(file)

    paragraphs, lines = get_data(data['Blocks'])
    
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
        if gpt_is_caption(paragraph[0]):
            for id in paragraph[1]:
                if lines[id][-1] is not True:
                    lines[id].append(True)
        
        for id in paragraph[1]:
            line = lines.get(id, "")
            points = []
            for point in line[2]:
                points.append(point['X'])
                points.append(point['Y'])
            line_polygon = Polygon(points)
            if is_line_inside_figure(line_polygon, figuresPolygons):
                if lines[id][-1] is not True:
                    lines[id].append(True)
            line_content = line[0]
            line_confidence = line[1]
            line_polygons = [line_polygon]
            if len(line) == 3:
                lines_result.append(Line(polygons=line_polygons, content=line_content, confidence=line_confidence))
            else:
                assert len(line) == 4 and line[-1] is True
                lines_result.append(Line(polygons=line_polygons, content=line_content, confidence=line_confidence, is_caption=True))

    return lines_result

if __name__ == "__main__":
    input_folder = "json"
    output_folder = "tmp"
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            input_path = os.path.join(input_folder, filename)
            lines = extract_lines(input_path)
            
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write("\n".join(line.content for line in lines))
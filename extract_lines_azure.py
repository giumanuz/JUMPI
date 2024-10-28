import json
from commons import Polygon, Line, is_line_inside_figure, gpt_correct_line, gpt_is_caption
import os

def is_line_in_captions(line_spans: list[dict], captions_spans: list[tuple]) -> bool:
    line_start = min(span["offset"] for span in line_spans)
    line_end = max(span["offset"] + span["length"] for span in line_spans)
    for caption_offset, caption_length in captions_spans:
        caption_start = caption_offset
        caption_end = caption_offset + caption_length
        if (line_start < caption_end) and (line_end > caption_start):
            return True
    return False

def get_confidence(line_spans: list[dict], words: list[dict]) -> float:
    line_start = min(span["offset"] for span in line_spans)
    line_end = max(span["offset"] + span["length"] for span in line_spans)

    low = 0
    high = len(words)
    while low + 1 < high:
        mid = (low + high) // 2
        if words[mid]["span"]["offset"] <= line_start:
            low = mid
        else:
            high = mid
    
    confidence = 0
    word_cnt = 0
    for i in range(low, len(words)):
        word = words[i]
        word_span = word["span"]
        word_offset = word_span["offset"]
        word_length = word_span["length"]
        word_end = word_offset + word_length

        if (line_start <= word_offset) and (word_end <= line_end):
            confidence += word["confidence"]
            word_cnt += 1
        
        if line_end < word_end:
            break

    return confidence / word_cnt if word_cnt > 0 else 0

def extract_lines(file_path: str) -> list[Line]:
    with open(file_path, 'r') as file:
        data = json.load(file)

    whole_text = data["analyzeResult"]["content"]

    figuresPolygons = [] # if the polygon of a line is inside a figure, the text will be skipped
    captionsSpans = [] # span is a pair of {offset, length}. You can get the content using whole_text[offset:offset+length]

    for figure in data["analyzeResult"].get("figures", []):
        for boundingRegion in figure.get("boundingRegions", []):
            figuresPolygons.append(Polygon(boundingRegion["polygon"]))
        caption = figure.get("caption", {})
        for span in caption.get("spans", []):
            captionsSpans.append((span["offset"], span["length"]))

    for paragraph in data["analyzeResult"].get("paragraphs", []):
        result = gpt_is_caption(whole_text, paragraph.get("content", ""))
        # TODO: should we remove the page number?
        if result or paragraph.get("role", "") == "pageNumber":
            for span in paragraph.get("spans", []):
                captionsSpans.append((span["offset"], span["length"]))

    lines = []
    words = [page.get("words", []) for page in data["analyzeResult"].get("pages", [])]

    for page_idx in range(len(data["analyzeResult"].get("pages", []))):
        for line in data["analyzeResult"]["pages"][page_idx].get("lines", []):
            line_polygon = Polygon(line["polygon"])
            line_spans = line.get("spans", [])
            line_content = line.get("content", "")

            if is_line_inside_figure(line_polygon, figuresPolygons):
                continue

            if is_line_in_captions(line_spans, captionsSpans):
                continue

            line_confidence = get_confidence(line_spans, words[page_idx])
            line_polygons = [line_polygon]
            line_content = gpt_correct_line(whole_text, line_content)
            new_line = Line(
                polygons=line_polygons, 
                content=line_content, 
                confidence=line_confidence, 
                spans=[(span["offset"], span["length"]) for span in line_spans]
            )
            lines.append(new_line)

    return lines

# if __name__ == "__main__":
#     input_folder = "azure-json"
#     output_folder = "azure-lines"
#     os.makedirs(output_folder, exist_ok=True)
    
#     for filename in os.listdir(input_folder):
#         if filename.endswith(".json"):
#             input_path = os.path.join(input_folder, filename)
#             lines = extract_lines(input_path)
            
#             output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
#             with open(output_path, "w") as output_file:
#                 for line in lines:
#                     output_file.write(line.content + "\n")
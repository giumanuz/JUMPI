import json

from commons import Polygon, Line


def compute_overlap_percentage(polygon1: Polygon, polygon2: Polygon) -> float:
    shapely_poly1 = polygon1.to_shapely()
    shapely_poly2 = polygon2.to_shapely()
    if not shapely_poly1.is_valid or not shapely_poly2.is_valid:
        return 0
    intersection_area = shapely_poly1.intersection(shapely_poly2).area
    poly1_area = shapely_poly1.area
    if poly1_area == 0:
        return 0
    return intersection_area / poly1_area


def is_line_inside_figure(line_polygon: Polygon, figures_polygons: list[Polygon], threshold: float = 0.9) -> bool:
    overlap_percentage = 0
    for figure_polygon in figures_polygons:
        overlap_percentage += compute_overlap_percentage(line_polygon, figure_polygon)
    return overlap_percentage >= threshold


def gpt_is_caption(paragraph: str) -> bool:
    # TODO: Only for testing purposes
    return False


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

    figure_polygons = []  # if the polygon of a line is inside a figure, the text will be skipped
    caption_spans = []  # span is a pair of {offset, length}. You can get the content using whole_text[offset:offset+length]
    offset_page_number = []  # in this way I can idenfy the page number and skip it

    for figure in data.get("figures", []):
        for boundingRegion in figure.get("boundingRegions", []):
            figure_polygons.append(Polygon(boundingRegion["polygon"]))
        caption = figure.get("caption", {})
        for span in caption.get("spans", []):
            caption_spans.append((span["offset"], span["length"]))

    for paragraph in data.get("paragraphs", []):
        if paragraph.get("role", "") == "pageNumber":
            offset_page_number.append(paragraph.get("spans", [])[0]["offset"])
            continue
        paragraph_decoded = repr(paragraph.get("content", ""))[1:-1]
        result = gpt_is_caption(paragraph_decoded)
        if result:
            for span in paragraph.get("spans", []):
                caption_spans.append((span["offset"], span["length"]))

    lines = []
    words = [page.get("words", []) for page in data.get("pages", [])]

    for page_idx in range(len(data.get("pages", []))):
        for line in data["pages"][page_idx].get("lines", []):
            line_polygon = Polygon(line["polygon"])
            line_spans = line.get("spans", [])
            line_content = repr(line.get("content", ""))[1:-1]
            line_is_caption = False

            if line_spans[0]["offset"] in offset_page_number:
                continue

            if is_line_inside_figure(line_polygon, figure_polygons):
                continue

            if is_line_in_captions(line_spans, caption_spans):
                line_is_caption = True

            line_confidence = get_confidence(line_spans, words[page_idx])
            line_polygons = [line_polygon]
            lines.append(Line(
                polygons=line_polygons,
                content=line_content,
                confidence=line_confidence,
                spans=[(span["offset"], span["length"]) for span in line_spans],
                is_caption=line_is_caption
            ))

    return lines

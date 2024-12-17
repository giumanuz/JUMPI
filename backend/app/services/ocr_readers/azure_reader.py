from base64 import b64encode
import json
import logging
import os
from pathlib import Path

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.credentials import AzureKeyCredential
from flask import Config

from app.services.ocr_readers.ocr_reader import OcrReader
from app.utils.classes import ArticleFigure
from commons import Line, Polygon


def _get_confidence(line_spans: list[dict], words: list[dict]) -> float:
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


def _compute_overlap_percentage(polygon1: Polygon, polygon2: Polygon) -> float:
    shapely_poly1 = polygon1.to_shapely()
    shapely_poly2 = polygon2.to_shapely()
    if not shapely_poly1.is_valid or not shapely_poly2.is_valid:
        return 0
    intersection_area = shapely_poly1.intersection(shapely_poly2).area
    poly1_area = shapely_poly1.area
    if poly1_area == 0:
        return 0
    return intersection_area / poly1_area


class AzureDiReader(OcrReader):
    logger = logging.getLogger(__name__)

    def __init__(self, image_path):
        super().__init__(image_path)
        self.json_result_filename = Path(self.image_path).stem + ".json"
        self.__figure_polygons = []
        self.__caption_spans = []
        self.__page_offsets = []
        AZURE_DI_ENDPOINT = 'https://mdp-test.cognitiveservices.azure.com/'
        AZURE_DI_API_KEY = os.getenv('DOCUMENTINTELLIGENCE_API_KEY')

        self.client = DocumentIntelligenceClient(
            endpoint=AZURE_DI_ENDPOINT,
            credential=AzureKeyCredential(AZURE_DI_API_KEY)
        )

    def read_to_file(self, output_dir: str):
        result = self.__analyze_document()
        output_file_path = Path(output_dir) / self.json_result_filename
        self.__save_result_to_file(result, output_file_path)

    def get_lines(self) -> list[Line]:
        with open(self.image_path, 'r') as file:
            data = json.load(file)

        for figure in data.get("figures", []):
            for boundingRegion in figure.get("boundingRegions", []):
                self.__figure_polygons.append(
                    Polygon(boundingRegion["polygon"]))
            caption = figure.get("caption", {})
            for span in caption.get("spans", []):
                self.__caption_spans.append((span["offset"], span["length"]))

        for paragraph in data.get("paragraphs", []):
            if paragraph.get("role", "") == "pageNumber":
                self.__page_offsets.append(
                    paragraph.get("spans", [])[0]["offset"])
                continue
            # result = repr(paragraph.get("content", ""))[1:-1]
            # if gpt_is_caption(result):
            for span in paragraph.get("spans", []):
                self.__caption_spans.append((span["offset"], span["length"]))

        lines = []
        words = [page.get("words", []) for page in data.get("pages", [])]

        for page_idx in range(len(data.get("pages", []))):
            for line in data["pages"][page_idx].get("lines", []):
                line_polygon = Polygon(line["polygon"])
                line_spans = line.get("spans", [])
                line_content = repr(line.get("content", ""))[1:-1]
                line_is_caption = False

                if line_spans[0]["offset"] in self.__page_offsets:
                    continue
                if self.__is_line_inside_figure(line_polygon):
                    continue
                if self.__is_line_in_captions(line_spans):
                    line_is_caption = True

                line_confidence = _get_confidence(line_spans, words[page_idx])
                line_polygons = [line_polygon]
                lines.append(Line(
                    polygons=line_polygons,
                    content=line_content,
                    confidence=line_confidence,
                    spans=[(span["offset"], span["length"])
                           for span in line_spans],
                    is_caption=line_is_caption
                ))

        return lines

    @classmethod
    def get_figures(cls) -> list[ArticleFigure]:
        for file_path in Path(Config.AZURE_FOLDER).iterdir():
            with file_path.open('r') as f:
                data = json.load(f)

            name_file = file_path.name
            image = Path(Config.IMAGE_FOLDER) / name_file

            figures = []
            for figure in data.get("figures", []):
                boundingRegions = figure.get("boundingRegions", [])
                polygon = Polygon(boundingRegions["polygon"])
                image_polygon = cls._crop_image(image, polygon)
                caption = figure.get(
                    "caption", {}) or figure.get("footnotes", {})
                caption_content = caption.get("content", "")

                article_figure = ArticleFigure(
                    page=boundingRegions.get("pageNumber", -1),
                    caption=caption_content,
                    image_data=b64encode(
                        image_polygon.tobytes()).decode('utf-8')
                )
                figures.append(article_figure)

            return figures

    def __analyze_document(self) -> AnalyzeResult:
        try:
            return self.__try_analyze_document()
        except Exception as e:
            self.logger.error(f"Error during document analysis: {e}")
            raise Exception(f"Error during document analysis: {e}")

    def __try_analyze_document(self) -> AnalyzeResult:
        with open(self.image_path, "rb") as f:
            poller = self.client.begin_analyze_document(
                "prebuilt-layout",
                analyze_request=f,
                content_type="application/octet-stream"
            )
        return poller.result()

    def __save_result_to_file(self, result: AnalyzeResult, output_file: Path):
        try:
            with open(output_file, 'w') as f:
                json.dump(result.as_dict(), f, indent=4)
            self.logger.debug(f"Result saved in: {output_file}")
            return output_file
        except Exception as e:
            self.logger.error(f"Error saving result to file: {e}")
            raise e

    def __is_line_inside_figure(self, line_polygon: Polygon, threshold: float = 0.9) -> bool:
        overlap_percentage = 0
        for figure_polygon in self.__figure_polygons:
            overlap_percentage += _compute_overlap_percentage(
                line_polygon, figure_polygon)
        return overlap_percentage >= threshold

    def __is_line_in_captions(self, line_spans: list[dict]) -> bool:
        line_start = min(span["offset"] for span in line_spans)
        line_end = max(span["offset"] + span["length"] for span in line_spans)
        for caption_offset, caption_length in self.__caption_spans:
            caption_start = caption_offset
            caption_end = caption_offset + caption_length
            if (line_start < caption_end) and (line_end > caption_start):
                return True
        return False

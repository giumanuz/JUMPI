from base64 import b64encode
import logging
import os
from PIL import Image, ImageDraw
import numpy

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.credentials import AzureKeyCredential

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
        self.__figure_polygons = []
        self.__caption_spans = []
        self.__page_offsets = []
        AZURE_DI_ENDPOINT = 'https://mdp-test.cognitiveservices.azure.com/'
        AZURE_DI_API_KEY = os.getenv('DOCUMENTINTELLIGENCE_API_KEY')

        self.client = DocumentIntelligenceClient(
            endpoint=AZURE_DI_ENDPOINT,
            credential=AzureKeyCredential(AZURE_DI_API_KEY)
        )

    def load_json(self) -> None:
        result = self.__analyze_document()
        self.json_data = result.as_dict()

    # TODO: Rivedere la parte delle caption e delle figure perche con la caption che detectioamo che ssono dentro una figura non ci stiamo facendo niente
    def get_lines(self) -> list[Line]:
        for figure in self.json_data.get("figures", []):
            for boundingRegion in figure.get("boundingRegions", []):
                self.__figure_polygons.append(
                    Polygon(boundingRegion["polygon"]))
            caption = figure.get("caption", {})
            for span in caption.get("spans", []):
                self.__caption_spans.append((span["offset"], span["length"]))

        for paragraph in self.json_data.get("paragraphs", []):
            if paragraph.get("role", "") == "pageNumber":
                self.__page_offsets.append(
                    paragraph.get("spans", [])[0]["offset"])
                continue
            # result = repr(paragraph.get("content", ""))[1:-1]
            # if gpt_is_caption(result):
            for span in paragraph.get("spans", []):
                self.__caption_spans.append((span["offset"], span["length"]))

        lines = []
        words = [page.get("words", [])
                 for page in self.json_data.get("pages", [])]

        for page_idx in range(len(self.json_data.get("pages", []))):
            for line in self.json_data["pages"][page_idx].get("lines", []):
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

    def get_figures(self) -> list[ArticleFigure]:
        figures = []
        for figure in self.json_data.get("figures", []):
            boundingRegions = figure.get("boundingRegions", [])
            polygon = Polygon(boundingRegions["polygon"])
            image_polygon = self._crop_image(self.image, polygon)
            caption = figure.get(
                "caption", {}) or figure.get("footnotes", {})
            caption_content = caption.get("content", "")

            # TODO: vedere se è corretto la base64 delle figures
            article_figure = ArticleFigure(
                page=boundingRegions.get("pageNumber", -1),
                caption=caption_content,
                image_data=b64encode(
                    image_polygon.tobytes()).decode('utf-8')
            )
            
            figures.append(article_figure)

        return figures

    def _crop_image(self, points: list[int], image: Image) -> Image:
        imArray = numpy.asarray(image)
        maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
        ImageDraw.Draw(maskIm).polygon(points, outline=1, fill=1)
        mask = numpy.array(maskIm)
        newImArray = numpy.empty(imArray.shape, dtype='uint8')

        newImArray[:, :, :3] = imArray[:, :, :3]

        newImArray[:, :, 3] = mask*255

        return Image.fromarray(newImArray, "RGBA")

    def __analyze_document(self) -> AnalyzeResult:
        try:
            return self.__try_analyze_document()
        except Exception as e:
            self.logger.error(f"Error during document analysis: {e}")
            raise Exception(f"Error during document analysis: {e}")

    def __try_analyze_document(self) -> AnalyzeResult:
        image_bytes = self._process_file_to_bytes()
        poller = self.client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=image_bytes,
            content_type="application/octet-stream"
        )
        return poller.result()

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

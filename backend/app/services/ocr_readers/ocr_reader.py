from abc import ABC, abstractmethod
import numpy
from PIL import Image, ImageDraw

from app.utils.classes import ArticleFigure
from commons import Line
from PIL import Image


class OcrReader(ABC):
    def __init__(self, image_path):
        self.image_path = image_path

    @abstractmethod
    def read_to_file(self, output_file_path: str):
        ...

    @abstractmethod
    def get_lines(self) -> list[Line]:
        ...

    @staticmethod
    def _crop_image(points: list[int], image: Image) -> Image:
        imArray = numpy.asarray(image)
        maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
        ImageDraw.Draw(maskIm).polygon(points, outline=1, fill=1)
        mask = numpy.array(maskIm)
        newImArray = numpy.empty(imArray.shape, dtype='uint8')

        newImArray[:, :, :3] = imArray[:, :, :3]

        newImArray[:, :, 3] = mask*255

        return Image.fromarray(newImArray, "RGBA")

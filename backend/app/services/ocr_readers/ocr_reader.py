from abc import ABC, abstractmethod
from werkzeug.utils import secure_filename
from io import BytesIO
from PIL import Image, UnidentifiedImageError

from werkzeug.datastructures import FileStorage
from app.utils.classes import ArticleFigure
from commons import Line
from PIL import Image


class OcrReader(ABC):
    def __init__(self, file: FileStorage):
        # TODO: vedere se serve veramente il file
        self.file: FileStorage = file
        self.image: Image = Image.open(file)
        self.json_data: dict = None
        self.file_name: str = secure_filename(file.filename)

    @abstractmethod
    def load_json(self, output_file_path: str):
        ...

    @abstractmethod
    def get_lines(self) -> list[Line] | list[str]:
        ...

    @abstractmethod
    def get_figures(self) -> list[ArticleFigure]:
        ...

    def _process_file_to_bytes(self) -> bytes:
        try:
            self.logger.debug(f"Opening file: {self.file_name}")
            image = Image.open(self.file.stream)

            if image.format not in ["JPEG", "PNG"]:
                self.logger.warning(f"File {self.file_name} is {image.format}. Converting to PNG.")
                buffer = BytesIO()
                image.convert("RGB").save(buffer, format="PNG")
                buffer.seek(0)
                return buffer.getvalue()
            else:
                self.logger.debug(f"File format: {image.format}")
                buffer = BytesIO()
                image.save(buffer, format=image.format)
                buffer.seek(0)
                return buffer.getvalue()
        except UnidentifiedImageError:
            self.logger.error(f"File {self.file_name} is not a valid image.")
            raise ValueError(
                "The uploaded file is not a valid image or is corrupted.")

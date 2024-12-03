from abc import ABC, abstractmethod

from commons import Line


class OcrReader(ABC):
    def __init__(self, image_path):
        self.image_path = image_path

    @abstractmethod
    def read_to_file(self, output_file_path: str):
        ...

    @abstractmethod
    def get_lines(self) -> list[Line]:
        ...

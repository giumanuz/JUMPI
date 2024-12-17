import logging
import os
import boto3
from werkzeug.datastructures import FileStorage

from app.services.ocr_readers.ocr_reader import OcrReader


class AwsTextractReader(OcrReader):
    logger = logging.getLogger(__name__)

    def __init__(self, file: FileStorage):
        super().__init__(file)
        self.textract = boto3.client(
            'textract',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION")
        )

    def load_json(self) -> None:
        image_bytes = self._process_file_to_bytes()
        response = self.__analyze_document(image_bytes)
        self.json_data = response

    def get_lines(self) -> list[str]:
        lines = []
        for block in self.json_data.get('Blocks', []):
            if block.get('BlockType') == 'LINE':
                lines.append(str(block["Text"]))
        return lines

    def get_figures(self):
        pass

    def __analyze_document(self, image_bytes):
        try:
            self.logger.debug(f"Analyzing image {self.file_name}")
            if not image_bytes:
                raise ValueError("Image file is empty or corrupted")
            response = self.textract.analyze_document(
                Document={'Bytes': image_bytes},
                FeatureTypes=['LAYOUT']
            )
            return response
        except boto3.exceptions.ClientError as e:
            self.logger.error(f"AWS ClientError: {e}")
            raise Exception(f"AWS ClientError: {e}")
        except Exception as e:
            self.logger.error(f"Error during document analysis: {e}")
            raise Exception(f"Error during document analysis: {e}")
        finally:
            self.logger.debug(f"Finished analyzing image {self.file_name}")

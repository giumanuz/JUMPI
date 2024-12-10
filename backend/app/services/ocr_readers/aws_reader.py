import base64
import json
import logging
import os
from pathlib import Path

import boto3

from app.services.ocr_readers.ocr_reader import OcrReader
from commons import Line


class AwsTextractReader(OcrReader):
    logger = logging.getLogger(__name__)

    def __init__(self, image_path):
        super().__init__(image_path)
        self.textract = boto3.client(
            'textract',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION")
        )
        self.json_result_filename = Path(self.image_path).stem + ".json"

    def read_to_file(self, output_dir: str):
        with open(self.image_path, 'rb') as document:
            image_bytes = document.read()
        output_file = Path(output_dir) / self.json_result_filename
        response = self.__analyze_document(image_bytes)
        self.__save_result_to_file(response, output_file)

    def get_lines(self) -> list[Line]:
        with open(self.json_result_filename, 'r') as file:
            data = json.load(file)['Blocks']
        return [str(block["Text"]) for block in data if block['BlockType'] == 'LINE']

    def __analyze_document(self, image_bytes):
        try:
            self.logger.debug(f"Analyzing image {self.image_path}")
            return self.textract.analyze_document(
                Document={'Bytes': image_bytes},
                FeatureTypes=['LAYOUT']
            )
        except Exception as e:
            self.logger.error(f"Error during document analysis: {e}")
            raise Exception(f"Error during document analysis: {e}")
        finally:
            self.logger.debug(f"Finished analyzing image {self.image_path}")

    def __save_result_to_file(self, response, output_file):
        try:
            with open(output_file, 'w') as f:
                json.dump(response, f, indent=4)
            self.logger.debug(f"Result saved in: {output_file}")
        except Exception as e:
            self.logger.error(f"Error saving result to file: {e}")
            raise e



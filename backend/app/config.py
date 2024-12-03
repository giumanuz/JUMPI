import os
from dataclasses import dataclass


@dataclass
class Config:
    TEMP_FOLDER = './temp'
    IMAGE_FOLDER = f'{TEMP_FOLDER}/images'
    IMAGE_COMPARISON_FOLDER = f'{TEMP_FOLDER}/images_comparison'
    AWS_FOLDER = f'{TEMP_FOLDER}/aws'
    AZURE_FOLDER = f'{TEMP_FOLDER}/azure'
    REPORT_FOLDER = f'{TEMP_FOLDER}/reports'
    GPT_FOLDER = f'{TEMP_FOLDER}/gpt'

    ELASTIC_URL = os.getenv('ELASTIC_URL')

    @classmethod
    def create_temp_dirs(cls):
        from pathlib import Path
        folders = [
            cls.TEMP_FOLDER,
            cls.IMAGE_FOLDER,
            cls.IMAGE_COMPARISON_FOLDER,
            cls.AWS_FOLDER,
            cls.AZURE_FOLDER,
            cls.REPORT_FOLDER,
            cls.GPT_FOLDER,
        ]
        for folder in folders:
            Path(folder).mkdir(parents=True, exist_ok=True)

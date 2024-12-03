import json
import os
from pathlib import Path

import boto3
from dotenv import load_dotenv

PATH_TO_IMAGE = "../images/2.jpg"
PATH_OUTPUT_FOLDER = "json"


def analyze_document(file_path=PATH_TO_IMAGE, output_path=PATH_OUTPUT_FOLDER):
    load_dotenv(dotenv_path="../.env")
    textract = boto3.client(
        'textract',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION")
    )

    with open(file_path, 'rb') as document:
        image_bytes = document.read()

    try:
        response = textract.analyze_document(
            Document={'Bytes': image_bytes},
            FeatureTypes=['LAYOUT']
        )

        output_file = Path(output_path) / (Path(file_path).stem + ".json")
        with open(output_file, 'w') as f:
            json.dump(response, f, indent=4)

        print(f"Result saved in: {output_file}")
    except Exception as e:
        print(f"Error during document analysis: {e}")

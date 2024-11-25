import boto3
import json
from dotenv import load_dotenv
import os

PATH_TO_IMAGE = "../images/2.jpg"
PATH_OUTPUT_FOLDER = "json"
AWS_TEXTRACT_FOLDER = "aws-textract"


def analyze_local_document(file_path=PATH_TO_IMAGE, feature_types=["LAYOUT"], output_path=PATH_OUTPUT_FOLDER):
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
            FeatureTypes=feature_types
        )

        output_file = f"{output_path}/{file_path.split('/')[-1].split('.')[0]}_NEW.json"
        with open(output_file, 'w') as f:
            json.dump(response, f, indent=4)

        print(f"Risultato salvato in: {output_file}")
    except Exception as e:
        print(f"Errore durante l'analisi del documento: {e}")


if __name__ == "__main__":
    analyze_local_document(PATH_TO_IMAGE, ["LAYOUT"])

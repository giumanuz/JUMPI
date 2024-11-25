import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.exceptions import HttpResponseError
from dotenv import load_dotenv
import json


PATH_TO_IMAGE = "../images/2.jpg"
PATH_OUTPUT_FOLDER = "json"


def analyze_layout(path_to_sample_document=PATH_TO_IMAGE, output_path=PATH_OUTPUT_FOLDER):
    load_dotenv(dotenv_path="../.env")

    endpoint = 'https://mdp-test.cognitiveservices.azure.com/'
    key = os.getenv('DOCUMENTINTELLIGENCE_API_KEY')

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    try:
        with open(path_to_sample_document, "rb") as f:
            poller = document_intelligence_client.begin_analyze_document(
                "prebuilt-layout",
                analyze_request=f,
                content_type="application/octet-stream"
            )
        result: AnalyzeResult = poller.result()
        output_file_path = os.path.join(output_path, os.path.basename(path_to_sample_document).replace('.jpg', '_NEW.json'))
        with open(output_file_path, 'w') as output_file:
            json.dump(result.as_dict(), output_file, indent=4)
                
        print(f"Result saved in: {output_file_path}")
    except Exception as e:
        print(f"Error during document analysis: {e}")



if __name__ == "__main__":

    try:
        load_dotenv(dotenv_path="../.env")
        analyze_layout()
    except HttpResponseError as error:
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            if error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            raise
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        raise

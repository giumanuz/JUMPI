import json


# Documentation: https://docs.aws.amazon.com/textract/latest/dg/layoutresponse.html
def extract_lines(file_path: str) -> list[str]:
    with open(file_path, 'r') as file:
        data = json.load(file)['Blocks']
    return [repr(_["Text"])[1:-1] for _ in data if _['BlockType'] == 'LINE']

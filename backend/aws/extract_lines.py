import json, os

# some documentation: https://docs.aws.amazon.com/textract/latest/dg/layoutresponse.html
def extract_lines(file_path: str) -> list[str]:
    with open(file_path, 'r') as file:
        data = json.load(file)['Blocks']
    lines = [repr(_["Text"])[1:-1] for _ in data if _['BlockType'] == 'LINE']
    return lines

if __name__ == "__main__":
    input_folder = "json"
    output_folder = "tmp"
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            input_path = os.path.join(input_folder, filename)
            lines = extract_lines(input_path)
            
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write("\n".join(line for line in lines))
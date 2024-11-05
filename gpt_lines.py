import os
from functools import cache

from openai import OpenAI
from dotenv import load_dotenv
from extract_lines_azure import extract_lines as extract_lines_azure
from extract_lines_aws import extract_lines as extract_lines_aws
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def main():
    input_folder = 'aws-json'
    output_folder = 'aws-gpt-lines'
    process_files_in_parallel(input_folder, output_folder)


def process_file_and_get_result(filepath: str) -> tuple[str, str]:
    if 'azure' in filepath:
        file_lines = "\n".join([line.content for line in extract_lines_azure(filepath)])
    elif 'aws' in filepath:
        file_lines = "\n".join([line.content for line in extract_lines_aws(filepath)])
    response = call_api(file_lines)
    return response, filepath


@cache
def get_correction_system_prompt() -> str:
    with open("gpt_prompt.md", "r") as f:
        return f.read()


def call_api(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": get_correction_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096,
            temperature=0.2
        )
        content = response.choices[0].message.content
        return "\n".join((l.strip() for l in content.split("\n")))
    except Exception as e:
        print(f"Error in API request: {e}")
        return None


def process_files_in_parallel(input_folder: str, output_folder: str):
    filepaths = []
    for filename in os.listdir(input_folder):
        filepath = os.path.join(input_folder, filename)
        if not os.path.isfile(filepath):
            continue
        filepaths.append(filepath)

    futures = []
    with ThreadPoolExecutor() as executor:
        for filepath in filepaths:
            future = executor.submit(process_file_and_get_result, filepath)
            futures.append(future)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for future in tqdm(as_completed(futures), total=len(futures), desc="Processing files"):
        corrected_content, filepath = future.result()
        output_filepath = filepath.replace(input_folder, output_folder).replace('.json', '.txt')
        with open(output_filepath, 'w', encoding='utf-8') as file:
            file.write(corrected_content)


if __name__ == '__main__':
    main()

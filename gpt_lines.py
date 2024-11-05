import os
from functools import cache

from openai import OpenAI
from dotenv import load_dotenv
from extract_lines_azure import extract_lines as extract_lines_azure
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

input_folder = 'azure-json'
output_folder = 'azure-gpt-lines'
NUMBER_OF_CONTEXT_LINES = 5

def main():
    process_file("azure-json/4.json")
    # for input_file in os.listdir(input_folder):
    #     print(f'Processing {input_file}')
    #     input_file_path = os.path.join(input_folder, input_file)
    #
    #     if '8' not in input_file:
    #         continue
    #
    #     if os.path.isfile(input_file_path):
    #         file_lines = [line.content for line in extract_lines_azure(input_file_path)]
    #
    #         corrected_lines = parallel_correct_text(file_lines, NUMBER_OF_CONTEXT_LINES)
    #
    #         output_path = os.path.join(output_folder, input_file.replace('.json', '.txt'))
    #
    #         with open(output_path, 'w', encoding='utf-8') as file:
    #             for line in corrected_lines:
    #                 file.write(line + '\n')
    #
    #         print(f'Corrected text saved in {output_path}')

def process_file(filepath: str) -> None:
    file_lines = "\n".join([line.content for line in extract_lines_azure(filepath)[:100]])
    # print(file_lines)
    # return
    response = call_api(file_lines)
    print(response)


if not os.path.exists(output_folder):
    os.makedirs(output_folder)


@cache
def get_correction_system_prompt() -> str:
    with open("gpt_prompt.md", "r") as f:
        return f.read()


def get_formatted_input(context: str, line: str) -> str:
    out = "<context>\n"
    for l in context.split("\n"):
        if l == line:
            out += f"<line>{l}</line>\n"
        else:
            out += f"{l}\n"
    out += "</context>"
    return out


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
        # print(response)
        return response.choices[0].message.content.strip().replace("  \n", "\n")
    except Exception as e:
        print(f"Error in API request: {e}")
        return None


def process_text(i, line: str, context: str):
    prompt = get_formatted_input(context, line)
    response = call_api(prompt)
    print(f"response: {response}")
    return i, response


def parallel_correct_text(lines, x):
    corrected_text = [None] * len(lines)

    with ThreadPoolExecutor() as executor:
        futures = {}

        for i in range(len(lines)):
            context_lines = lines[max(0, i - x) : min(len(lines), i + 1 + x)]
            context = "\n".join(context_lines)
            # context_text = " ".join(context_lines).replace('-\n', '').replace('\n', ' ')
            line = lines[i]
            futures[executor.submit(process_text, i, line, context)] = i

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing lines"):
            i, response = future.result()
            corrected_text[i] = response

    return corrected_text


if __name__ == '__main__':
    main()
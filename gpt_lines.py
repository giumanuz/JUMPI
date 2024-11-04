import os
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

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def generate_correction_prompt(line:str, context_text:str):
        return f"""
Analizza e correggi la seguente stringa estratta tramite OCR.

Restituisci solo la linea corretta in output correggendo solo grammatica, punteggiatura e caratteri speciali di questa singola linea senza alterare le parole o aggiungere testo extra. 

Fai attenzione a non includere né riferimenti né testo del contesto. Mantieni la frase intatta e correggi solo piccoli errori di caratteri, come punti al posto di virgole o virgolette francesi (« »). Non cambiare il significato o l'ordine delle parole e non inserire punti alla fine della frase se non ci sono. 

Se la linea da correggere termina con '-' non devi correggere la parola spezzata.

In output, restituisci solo la linea corretta, senza aggiungere nulla del contesto.

Contesto comprendente la linea da correggere: 
-------------------------------------------------------
{context_text}
-------------------------------------------------------
Linea da correggere:
-------------------------------------------------------
{line}
-------------------------------------------------------
"""

def call_api(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in API request: {e}")
        return None

def parallel_correct_text(text, x):
    corrected_text = [None] * len(text)

    def process_text(i, line:str, context_text:str):
        prompt = generate_correction_prompt(line, context_text)
        response = call_api(prompt)
        return i, response

    with ThreadPoolExecutor() as executor:
        futures = {}

        for i in range(len(text)):
            context_lines = text[max(0, i - x) : min(len(text), i + 1 + x)]
            context_text = " ".join(context_lines).replace('-\n', '').replace('\n', ' ')
            line = text[i]
            futures[executor.submit(process_text, i, line, context_text)] = i

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing lines"):
            i, response = future.result()
            corrected_text[i] = response

    return corrected_text

for input_file in os.listdir(input_folder):
    print(f'Processing {input_file}')
    input_file_path = os.path.join(input_folder, input_file)

    if '8' not in input_file:
        continue

    if os.path.isfile(input_file_path):
        file_lines = [line.content for line in extract_lines_azure(input_file_path)]
        
        corrected_lines = parallel_correct_text(file_lines, NUMBER_OF_CONTEXT_LINES)

        output_path = os.path.join(output_folder, input_file.replace('.json', '.txt'))

        with open(output_path, 'w', encoding='utf-8') as file:
            for line in corrected_lines:
                file.write(line + '\n')

        print(f'Corrected text saved in {output_path}')

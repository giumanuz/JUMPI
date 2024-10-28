import os
from openai import OpenAI
from dotenv import load_dotenv

# Carica le variabili di ambiente dal file .env
load_dotenv()

# Imposta la chiave API di OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Percorsi delle cartelle
input_folder = 'azure'
output_folder = 'azure-gpt'

# Crea la cartella di output se non esiste
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def rewrite_text(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f"Modifica solamente eventuali errori grammaticali nel seguente testo, senza modificare la forma e lo stile: {text}"}
            ],
            max_tokens=4096,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Errore nella richiesta alle API: {e}")
        return None

for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        input_path = os.path.join(input_folder, filename)
        with open(input_path, 'r', encoding='utf-8') as file:
            text_to_rewrite = file.read()

        rewritten_text = rewrite_text(text_to_rewrite)
        
        if rewritten_text:
            output_path = os.path.join(output_folder, filename)
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(rewritten_text)
            
            print(f"Testo riscritto salvato in '{output_path}'")

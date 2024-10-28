import language_tool_python
from spellchecker import SpellChecker
import os

tool = language_tool_python.LanguageTool('it')
spell = SpellChecker(language='it')

input_folder = 'aws'
output_folder = 'aws-results'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def correct_spelling(text):
    words = text.split()
    corrected_words = [spell.correction(word) if word in spell else word for word in words]
    return " ".join(corrected_words)

for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        input_path = os.path.join(input_folder, filename)
        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()

        spelling_corrected_text = correct_spelling(text)
        matches = tool.check(spelling_corrected_text)
        final_corrected_text = language_tool_python.utils.correct(spelling_corrected_text, matches)

        output_path = os.path.join(output_folder, filename)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(final_corrected_text)

        print(f"Correzione completata per {filename}. Risultato salvato in {output_path}")

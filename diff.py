import difflib
import os

input_folder_aws = 'aws'
input_folder_texts = 'azure'
output_folder = 'diff-results'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def find_word_differences(text1, text2):
    # Divide i testi in parole
    words1 = text1.split()
    words2 = text2.split()
    
    # Utilizza SequenceMatcher per confrontare le parole
    matcher = difflib.SequenceMatcher(None, words1, words2)
    differences = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':  # Parole nella stessa posizione, ma diverse
            for w1, w2 in zip(words1[i1:i2], words2[j1:j2]):
                differences.append(f"{w1} -> {w2}")
        elif tag == 'delete':  # Parole presenti solo nel primo testo (AWS)
            differences.append(f"- {' '.join(words1[i1:i2])}")
        elif tag == 'insert':  # Parole presenti solo nel secondo testo (Texts)
            differences.append(f"+ {' '.join(words2[j1:j2])}")
        elif tag == 'equal':  # Parole uguali
            pass
        else:
            print(f"Tag non riconosciuto: {tag}, {words1[i1:i2]}, {words2[j1:j2]}")

    return differences

for filename in os.listdir(input_folder_aws):
    # Ignora i file che finiscono con '-azure'
    if filename.endswith('.txt') and not filename.endswith('-azure.txt'):
        base_name = filename.replace('.txt', '')
        corresponding_file = f"{base_name}.md"

        aws_path = os.path.join(input_folder_aws, filename)
        texts_path = os.path.join(input_folder_texts, corresponding_file)

        if os.path.exists(texts_path):
            with open(aws_path, 'r', encoding='utf-8') as aws_file:
                aws_content = aws_file.read()

            with open(texts_path, 'r', encoding='utf-8') as texts_file:
                texts_content = texts_file.read()

            # Trova le differenze tra le parole
            word_differences = find_word_differences(aws_content, texts_content)

            # Salva i risultati in un file di output
            output_path = os.path.join(output_folder, f"{base_name}-diff.txt")
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write("\n".join(word_differences))

            print(f"Differenze di parole salvate in '{output_path}'.")

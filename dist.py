from Levenshtein import distance, ratio
import os
import pandas as pd

input_folder_azure = 'azure-gpt'
input_folder_aws = 'Texts'

levenshtein_results = []

for filename in os.listdir(input_folder_azure):
    if filename.endswith('-azure.txt'):
        base_name = filename.replace('-azure.txt', '')
        corresponding_file = f"{base_name}.md"  # nome file senza "-azure" nella cartella aws-gpt

        azure_path = os.path.join(input_folder_azure, filename)
        aws_path = os.path.join(input_folder_aws, corresponding_file)

        if os.path.exists(aws_path):
            with open(azure_path, 'r', encoding='utf-8') as azure_file:
                azure_content = azure_file.read()

            with open(aws_path, 'r', encoding='utf-8') as aws_file:
                aws_content = aws_file.read()

            lev_distance = ratio(azure_content, aws_content)
            levenshtein_results.append((filename, corresponding_file, lev_distance))

df = pd.DataFrame(levenshtein_results, columns=['Azure File', 'Testo', 'Levenshtein Ratio'])

print(df)

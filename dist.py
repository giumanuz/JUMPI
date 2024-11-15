from Levenshtein import distance, ratio
import os
import pandas as pd
 
folder1 = 'azure-lines'
folder2 = 'Texts-lines'
folder3 = 'merged-gpt-lines'
folder4 = 'Texts-lines'
 
levenshtein_results = []
 
for filename in os.listdir(folder1):
    file1 = os.path.join(folder1, filename)
    file2 = os.path.join(folder2, filename).replace('.txt', '.md')
    file3 = os.path.join(folder3, filename)
    file4 = os.path.join(folder4, filename).replace('.txt', '.md')
 
    if os.path.exists(file2) and os.path.exists(file3) and os.path.exists(file4):
        with open(file1, 'r', encoding='utf-8') as azure_lines_file:
            content_file_1 = "".join([line.strip() for line in azure_lines_file.readlines()])
 
        with open(file2, 'r', encoding='utf-8') as aws_lines_file:
            content_file_2 = "".join([line.strip() for line in aws_lines_file.readlines()])
 
        with open(file3, 'r', encoding='utf-8') as azure_gpt_file:
            content_file_3 = "".join([line.strip() for line in azure_gpt_file.readlines()])
 
        with open(file4, 'r', encoding='utf-8') as aws_gpt_file:
            content_file_4 = "".join([line.strip() for line in aws_gpt_file.readlines()])
 
        lev_distance_first = ratio(content_file_1, content_file_2)
        lev_distance_second = ratio(content_file_3, content_file_4)
        levenshtein_results.append((filename, lev_distance_first, lev_distance_second))

df = pd.DataFrame(levenshtein_results, columns=['Filename', 'azure', 'gpt'])
df = df.sort_values(by='Filename').reset_index(drop=True)
print('Comparison between azure with Original and gpt-merged with Original')
print(df.to_string(index=False))
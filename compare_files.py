import os
from Levenshtein import ratio
from pandas import DataFrame

'''
For each file in path1, if there is a corresponding file in path2, compare the similarity between the two files.
'''
def compare_files(path1, path2):
    levenshtein_results = []
    lengths = []

    for filename in os.listdir(path1):
        file1 = os.path.join(path1, filename)
        file2 = os.path.join(path2, filename)
        if not os.path.isfile(file2):
            continue
        with open(file1, 'r') as f:
            data1 = f.read()
        with open(file2, 'r') as f:
            data2 = f.read()
        levenshtein_results.append((filename, ratio(data1, data2)))
        lengths.append((filename, len(data1)))

    df = DataFrame(levenshtein_results, columns=['Filename', 'Similarity'])
    length_df = DataFrame(lengths, columns=['Filename', 'Length'])
    df = df.merge(length_df, on='Filename').sort_values(by='Filename').reset_index(drop=True)
    print(f'Similarity between {path1} and {path2}:\n')
    print(df.to_string(index=False))
    weighted_average = (df['Similarity'] * df['Length']).sum() / df['Length'].sum()
    print(f'\nWeighted average similarity: {weighted_average}')

if __name__ == '__main__':
    path1 = 'azure/gpt-lines'
    path2 = 'real/lines'
    compare_files(path1, path2)
import pandas as pd
import os

df = pd.read_csv(os.getcwd() + '/data-ingestion/simulated_loan_data.csv')

folder_name = 'folder_A'

folder_path = os.path.join(os.getcwd() + '/data-ingestion/', folder_name)

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

print(f"Folder '{folder_name}' is created at: {folder_path}")

chunk_size = 1000

chunks = [df[i:i + chunk_size] for i in range(0, df.shape[0], chunk_size)]

for i, chunk in enumerate(chunks):
    file_path = os.path.join(folder_path, f'chunk_{i+1}.csv')
    chunk.to_csv(file_path, index=False)
    print(f"Chunk {i+1} saved at: {file_path}")

print("Splitting completed successfully.")

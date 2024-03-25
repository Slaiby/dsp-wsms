import pandas as pd
import os
import numpy as np

def main():
    # Define the path to the parent directory of the script
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Define the path to the input directory containing the CSV files
    input_dir = os.path.join(parent_dir, "main-data-set")

    # Check if the input directory exists
    if not os.path.exists(input_dir):
        print("Input directory not found:", input_dir)
        return

    # Get the list of CSV files in the input directory
    csv_files = [file for file in os.listdir(input_dir) if file.endswith('.csv')]

    # Check if CSV files were found
    if not csv_files:
        print("No CSV files found in the directory:", input_dir)
        return
    else:
        print("CSV files found:", csv_files)

    # Iterate over each CSV file and process it
    for csv_file in csv_files:
        csv_file_path = os.path.join(input_dir, csv_file)
        print(f"Processing {csv_file}...")

        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)

        # Determine the number of rows in each chunk
        total_rows = len(df)
        rows_per_file = total_rows // 10  

        # Define the output directory for the processed data
        output_dir = os.path.join(parent_dir, "dags", "raw-data")
        os.makedirs(output_dir, exist_ok=True)

        # Split the DataFrame into chunks and save each chunk as a separate CSV file
        for i, chunk in enumerate(np.array_split(df, 10)):
            output_file_path = os.path.join(output_dir, f"{os.path.splitext(csv_file)[0]}_{i+1}.csv")
            chunk.to_csv(output_file_path, index=False)
            print(f"Chunk {i+1} saved to {output_file_path}")

if __name__ == '__main__':
    main()
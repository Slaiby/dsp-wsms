import subprocess
import os

def run_script(script_path):
    subprocess.run(['python', script_path], check=True)

def main():
    generate_data_script = os.getcwd() + '/data-ingestion/generate_new_data.py' 
    separate_data_script = os.getcwd() + '/data-ingestion/separate_into_data.py' 

    print("Generating new data...")
    run_script(generate_data_script)

    print("Separating data into folders...")
    run_script(separate_data_script)

    print("Setup completed successfully.")

if __name__ == "__main__":
    main()
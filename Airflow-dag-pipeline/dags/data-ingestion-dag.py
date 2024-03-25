from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import os
import random
import shutil

def read_data():
    # Get the directory where your DAG file resides
    dag_folder = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the raw-data folder
    raw_data_folder = os.path.join(dag_folder, 'raw-data')
    
    # Check if the folder exists and list files
    if os.path.exists(raw_data_folder):
        files = os.listdir(raw_data_folder)
        if files:
            file_name = random.choice(files)
            file_path = os.path.join(raw_data_folder, file_name)
            print("Selected file:", file_name)
            return file_path
        else:
            print("No files available in raw-data folder.")
    else:
        print("The raw-data folder does not exist.")

def save_file(**kwargs):
    file_path = kwargs['ti'].xcom_pull(task_ids='read_data')
    print("Received file path:", file_path)
    if file_path:
        good_data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "good-data") 
        shutil.move(file_path, good_data_folder)
        print(f"File moved to good-data folder: {file_path}")
    else:
        print("No files available in raw-data folder.")

default_args = {
   'owner': 'airflow123',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 24),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=1),
}

with DAG('data_ingestion_dag3.7', default_args=default_args, schedule_interval='* * * * *') as dag:
    read_data_task = PythonOperator(
        task_id='read_data',
        python_callable=read_data
    )

    save_file_task = PythonOperator(
        task_id='save_file',
        python_callable=save_file,
        provide_context=True
    )

    read_data_task >> save_file_task
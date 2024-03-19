import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def initialize_db():
    load_dotenv()

    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')

    params = {
        'dbname': 'postgres',
        'user': DB_USER,
        'password': DB_PASSWORD,
        'host': DB_HOST
    }

    with psycopg2.connect(**params) as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")
            if not cursor.fetchone():
                cursor.execute(f'CREATE DATABASE {DB_NAME};')
                print(f"Database '{DB_NAME}' created successfully.")
            else:
                print(f"Database '{DB_NAME}' already exists.")

    params['dbname'] = DB_NAME
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS api_inferences (
                    id SERIAL PRIMARY KEY,
                    inference_id VARCHAR(255) NOT NULL,
                    result JSONB NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            print("Table 'api_inferences' created/verified successfully.")
            conn.commit()
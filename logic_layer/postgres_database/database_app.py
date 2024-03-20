import json
import os
from logic_layer.postgres_database.database_utils import create_db_connection

async def insert_inference_data(conn, inference_id, result):
    await conn.execute('''
        INSERT INTO api_inferences (inference_id, result) VALUES ($1, $2)
    ''', inference_id, json.dumps(result))

async def initialize_db():
    DB_NAME = os.getenv('DB_NAME')

    conn = await create_db_connection()
    async with conn.transaction():
        exists = await conn.fetchval(f"SELECT EXISTS(SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}')")
        if not exists:
            await conn.execute(f'CREATE DATABASE {DB_NAME}')
            print(f"Database '{DB_NAME}' created successfully.")
        else:
            print(f"Database '{DB_NAME}' already exists.")
    await conn.close()

    conn = await create_db_connection()
    async with conn.transaction():
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS api_inferences (
                id SERIAL PRIMARY KEY,
                inference_id VARCHAR(255) NOT NULL,
                result JSONB NOT NULL,
                timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
            );
        ''')
        print("Table 'api_inferences' created/verified successfully.")
        
    await insert_inference_data(conn, 'example-inference-id-001', {'prediction': 'Approved', 'score': 0.95})
    await insert_inference_data(conn, 'example-inference-id-002', {'prediction': 'Denied', 'score': 0.35})

    print("Inserted example data into 'api_inferences' table.")
    await conn.close()

import json
from io import BytesIO
from fastapi import HTTPException, UploadFile

from logic_layer.acceptance_prediction.csv_service import validate_csv
from logic_layer.postgres_database.database_utils import create_db_connection

async def fetch_past_predictions(page=1, page_size=10):
    offset = (page - 1) * page_size
    conn = await create_db_connection()
    query = f'SELECT * FROM api_inferences ORDER BY timestamp DESC LIMIT {page_size} OFFSET {offset}'
    rows = await conn.fetch(query)
    await conn.close()
    return rows

async def insert_inference_data(data_input, prediction):
    conn = await create_db_connection()
    async with conn.transaction():
        await conn.execute('''
            INSERT INTO api_inferences (request_data, prediction) VALUES ($1, $2)
        ''', json.dumps(data_input), str(prediction))
    await conn.close()

async def handle_csv_file(file: UploadFile):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be CSV")

    file_content = await file.read()
    MAX_FILE_SIZE_BYTES = 200 * 1024 * 1024

    if len(file_content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="File size exceeds maximum limit")

    file_in_memory = BytesIO(file_content)
    is_valid, message = validate_csv(file_in_memory)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    file_in_memory.seek(0)
    return file_in_memory
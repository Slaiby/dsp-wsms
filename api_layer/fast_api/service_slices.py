import json
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
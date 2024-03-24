import json
from logic_layer.postgres_database.database_utils import create_db_connection

async def fetch_past_predictions():
    conn = await create_db_connection()
    rows = await conn.fetch('SELECT * FROM api_inferences')
    await conn.close()
    return rows

async def insert_inference_data(data_input, prediction):
    conn = await create_db_connection()
    async with conn.transaction():
        await conn.execute('''
            INSERT INTO api_inferences (request_data, prediction) VALUES ($1, $2)
        ''', json.dumps(data_input), str(prediction))
    await conn.close()
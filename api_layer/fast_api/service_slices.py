from logic_layer.postgres_database.database_utils import create_db_connection

async def fetch_past_predictions():
    conn = await create_db_connection()
    rows = await conn.fetch('SELECT * FROM api_inferences')
    await conn.close()
    return rows
import asyncpg
from database import config

conn = None


async def init():
    global conn
    conn = await asyncpg.connect(host=config.host, user=config.user, password=config.password, database=config.db_name)
    # with open('database/schema.sql', 'r', encoding='utf-8') as file:
    #     await conn.execute(file.read())


def get_conn():
    return conn

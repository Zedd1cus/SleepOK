import asyncpg
from database import config
from typing import Optional

pool: Optional[asyncpg.Pool] = None


async def init():
    global pool

    pool = await asyncpg.create_pool(**config.DB_SETTINGS)

    # with open('database/schema.sql', 'r', encoding='utf-8') as file:
    #     await conn.execute(file.read())


def get_poll():
    return pool

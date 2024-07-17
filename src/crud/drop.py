import os

import aiomysql
from src.crud.engine import db, host, port, user, password, engine, Base
from src.crud.models import UserRecord
from src.crud.queries.utils import add_object

ADMIN1_EMAIL = os.getenv("ADMIN1_EMAIL")
ADMIN1_PASSWORD = os.getenv("ADMIN1_PASSWORD")


async def close_db():
    await engine.dispose()


async def create_new_db():
    drop_query = "DROP DATABASE IF EXISTS %s;" % db
    create_query = "CREATE DATABASE %s" % db

    async with aiomysql.create_pool(
        host=host,
        port=port,
        user=user,
        password=password
    ) as pool:
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(drop_query)
                await cursor.execute(create_query)

        pool.close()
        await pool.wait_closed()

    async with engine.begin() as connection:
        # await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    user_record = UserRecord(
        name="Admin",
        email=ADMIN1_EMAIL,
        password=ADMIN1_PASSWORD,
        is_admin=1,
        enabled=1
    )
    await add_object(user_record)

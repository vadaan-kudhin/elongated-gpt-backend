import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.core.openai_queue import openai_queue
from src.crud.drop import close_db, create_new_db
from src.crud.queries.user import select_user_by_id


async def keep_resetting_db_conns():
    while True:
        await asyncio.sleep(3600)
        await select_user_by_id(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(keep_resetting_db_conns())
    asyncio.create_task(openai_queue.start())
    yield
    await close_db()

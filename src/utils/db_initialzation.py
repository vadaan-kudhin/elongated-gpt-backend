import asyncio
from src.crud.drop import create_new_db, close_db
from src.crud.engine import db, host, port, user, password


async def _main():
    await create_new_db()
    await close_db()


def main():
    asyncio.run(_main())

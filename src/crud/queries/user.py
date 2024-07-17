from sqlalchemy import select

from src.crud.models import UserRecord
from src.crud.queries.utils import scalar_selection


async def select_user_by_email(username: str) -> UserRecord | None:
    query = select(UserRecord).where(UserRecord.email == username)
    return await scalar_selection(query)


async def select_user_by_id(user_id: int) -> UserRecord | None:
    query = select(UserRecord).where(UserRecord.id == user_id)
    return await scalar_selection(query)


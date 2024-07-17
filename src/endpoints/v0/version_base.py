from typing import Annotated

from fastapi import APIRouter, Security
from src.endpoints.v0.users import router as users
from src.endpoints.v0.chat import router as chat
from src.schema.models import User
from src.security.security import (
    get_current_active_user
)

router = APIRouter(prefix="/v0")
router.include_router(users)
router.include_router(chat)


@router.get(
    "/users/me", response_model=User, tags=["Users"],
)
async def read_users_me(
        current_user: Annotated[
            User, Security(get_current_active_user, scopes=[])
        ]
):
    return current_user

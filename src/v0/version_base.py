from typing import Annotated

from fastapi import APIRouter, Security

from src.schema.models import User
from src.security.security import (
    get_current_active_user
)

router = APIRouter(prefix="/v0")


@router.get(
    "/users/me", response_model=User, tags=["Users"],
)
async def read_users_me(
        current_user: Annotated[
            User, Security(get_current_active_user, scopes=[])
        ]
):
    return current_user

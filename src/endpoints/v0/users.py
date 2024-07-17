from typing import Annotated

from fastapi import APIRouter, HTTPException, Security

from src.crud.models import UserRecord
from src.crud.queries.utils import add_object
from src.schema.factories.user_factory import UserFactory
from src.schema.models import User
from src.security.security import get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/user", status_code=201)
async def create_user(
        current_user: Annotated[
            User, Security(get_current_active_user, scopes=[])
        ],
        user: User
) -> User:
    if not user.is_admin:
        raise HTTPException(
            403, "Forbidden"
        )

    record = UserRecord(
        name=user.name,
        email=user.email,
        password="$2b$12$/6qqqQgfyMfPHwV73CKTSeHN6xKc3fCzGCz17VdtNydUWiE0kfDhG",
        is_admin=user.is_admin,
        enabled=user.enabled
    )
    await add_object(record)

    return UserFactory.create_full_user(record)

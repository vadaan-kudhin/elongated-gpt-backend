from datetime import timedelta
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.schema.factories.user_factory import UserFactory
from src.schema.security import Token
from src.security.security import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from src.utils.utils import lifespan
from src.endpoints.v0.version_base import router as v0


app = FastAPI(lifespan=lifespan)
app.include_router(v0)


@app.post(
    "/token", response_model=Token, tags=["Users"],
    status_code=201
)
async def login_for_access_token(
        form_data: Annotated[
            OAuth2PasswordRequestForm, Depends()
        ]
):
    """
    Create a token up to specification of Oauth2 Scope Authentication
    db tables are checked to see if the user should have those modules
    """
    user_data = await authenticate_user(
        form_data.username, form_data.password
    )

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = UserFactory.create_full_user(user_data)
    if not user.enabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Disabled account",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "full_name": user.name
        },
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

from datetime import timedelta, datetime
from typing import Annotated
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from starlette import status

from src.crud.models import UserRecord
from src.crud.queries.user import select_user_by_email
from src.schema.factories.user_factory import UserFactory
from src.schema.models import User
from src.schema.security import TokenData
from src.security.one_time_passwords import OTP
import os

from src.utils.mailing import EmailClient

# change with: ```openssl rand -hex 32```
SECRET_KEY = os.getenv("OAUTH2_SECRET")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_SECRET")  # Fernet.generate_key()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
PASSWORD_RESET_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("PASSWORD_RESET_TOKEN_EXPIRE_MINUTES")
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# EMAILS = EmailClient(
#     server=os.getenv("MAILING_SERVER"),
#     port=os.getenv("SMTP_PORT"),
#     username=os.getenv("MAILING_USERNAME"),
#     password=os.getenv("MAILING_PASSWORD"),
# )
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
)
password_reset_otp = OTP(os.environ.get("PASSWORD_RESET_OTP_SECRET"))


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def validate_token(
        token: str,
        exception: HTTPException,
) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        full_name: str = payload.get("full_name")

        if username is None:
            raise exception
        token_data = TokenData(
            username=username,
            full_name=full_name,
        )
    except InvalidTokenError:
        raise exception

    return token_data


async def authenticate_user(
        username: str, password: str
) -> UserRecord | bool:
    user = await select_user_by_email(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(
        data: dict, expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def _get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        security_scopes: SecurityScopes
) -> User:
    if security_scopes.scopes:
        authenticate_value = (
            f'Bearer scope="{security_scopes.scope_str}"'
        )
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    token_data = validate_token(
        token, credentials_exception
    )

    data = await select_user_by_email(username=token_data.username)

    if not data:
        raise credentials_exception

    user = UserFactory.create_full_user(data)

    return user


async def get_current_active_user(
    current_user: Annotated[
        User, Security(_get_current_user, scopes=[])
    ]
):
    if not current_user.enabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

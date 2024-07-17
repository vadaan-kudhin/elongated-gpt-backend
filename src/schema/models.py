from datetime import datetime
from enum import StrEnum
from typing import List

from pydantic import BaseModel, Field, EmailStr, field_validator

from src.schema.validation import basic_string_validation


class OpenAIModel(StrEnum):
    CHAT_GPT_35 = "CHAT_GPT_35"
    CHAT_GPT_4 = "CHAT_GPT_4"
    CHAT_GPT_4O = "CHAT_GPT_4O"


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str = Field(exclude=True)
    is_admin: bool
    class_name: str = "USER"
    enabled: bool

    @classmethod
    @field_validator("name", mode="before")
    def name_validation(cls, value: str):
        return basic_string_validation(value, "name")

    @classmethod
    @field_validator("password", mode="before")
    def password_validation(cls, value: str):
        return basic_string_validation(value, "password")


class PendingMessage(BaseModel):
    id: int
    chat_id: int
    user_input: str
    # response: str | None = None
    # timestamp: datetime | None = None
    class_name: str = "PENDING_MESSAGE"
    model: OpenAIModel

    @classmethod
    @field_validator("user_input", mode="before")
    def password_validation(cls, value: str):
        return basic_string_validation(value, "user_input")


class CompletedMessage(PendingMessage):
    response: str
    timestamp: datetime
    class_name: str = "COMPLETE_MESSAGE"


class Chat(BaseModel):
    id: int
    messages: List[PendingMessage]
    user: User
    class_name: str = "CHAT"


class Error(BaseModel):
    id: int
    error: str
    class_name: str = "ERROR"


class ResetRequest(BaseModel):
    email: EmailStr
    otp: str
    class_name: str = "RESET_REQUEST"

    @classmethod
    @field_validator("otp", mode="before")
    def otp_validation(cls, value: str):
        return basic_string_validation(value, "otp")

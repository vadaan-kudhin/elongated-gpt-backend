from pydantic import BaseModel, field_validator

from src.schema.validation import basic_string_validation


class TokenData(BaseModel):
    username: str
    full_name: str


class Token(BaseModel):
    access_token: str
    token_type: str

    @classmethod
    @field_validator("token_type", mode="before")
    def token_type_validation(cls, value: str):
        return basic_string_validation(value, "token_type")

    @classmethod
    @field_validator("access_token", mode="before")
    def access_token_type_validation(cls, value: str):
        return basic_string_validation(value, "access_token")

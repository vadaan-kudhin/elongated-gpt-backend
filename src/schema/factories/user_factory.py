from src.crud.models import UserRecord
from src.schema.models import User


class UserFactory:
    @staticmethod
    def create_full_user(record: UserRecord):
        return User(
            id=record.id,
            name=record.name,
            email=record.email,
            password=record.password,
            is_admin=record.is_admin,
            enabled=record.enabled,
        )

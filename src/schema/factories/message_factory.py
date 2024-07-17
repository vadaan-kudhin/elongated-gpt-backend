from fastapi import HTTPException

from src.crud.models import UserRecord
from src.schema.factories.user_factory import UserFactory
from src.schema.models import Chat, User, PendingMessage, OpenAIModel


class MessageFactory:
    @staticmethod
    def create_chat(chat_record, user_record):

        if type(user_record) is User:
            user = user_record
        elif type(user_record) is UserRecord:
            user = UserFactory.create_full_user(user_record)
        else:
            return HTTPException(
                500, "Unexpected data type for user_record"
            )

        return Chat(
            id=chat_record.id,
            messages=[],
            user=user
        )

    @staticmethod
    def create_message(message_record):
        return PendingMessage(
            id=message_record.id,
            chat_id=message_record.chat_id,
            user_input=message_record.user_input,
            model=message_record.model,
        )

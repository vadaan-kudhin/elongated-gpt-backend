from typing import Annotated

from fastapi import APIRouter, Security

from src.crud.models import UserRecord, ChatRecord, MessageRecord
from src.crud.queries.utils import add_object, add_objects
from src.schema.factories.message_factory import MessageFactory
from src.schema.models import User, Chat, PendingMessage
from src.security.security import get_current_active_user

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/message", status_code=201)
async def create_message(
        current_user: Annotated[
            User, Security(get_current_active_user, scopes=[])
        ],
        message: PendingMessage
) -> PendingMessage:

    if message.chat_id == 0:
        chat_record = ChatRecord(
                user_id=current_user.id
            )
        await add_object(chat_record)
        chat_id = chat_record.id
    else:
        chat_id = message.chat_id

    record = MessageRecord(
        id=0,
        chat_id=chat_id,
        user_input=message.user_input,
        model=message.model
    )
    await add_object(record)

    message = MessageFactory.create_message(record)
    return message

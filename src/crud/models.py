from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.mysql.types import BIT, INTEGER, TEXT

from src.crud.engine import Base


_COLLATION = "utf8mb4_general_ci"


class UserRecord(Base):
    __tablename__ = 'user'
    id = Column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
    )
    name = Column(
        String(50, collation=_COLLATION),
        nullable=False,
    )
    email = Column(
        String(50, collation=_COLLATION),
        unique=True,
        nullable=False,
    )
    password = Column(
        String(60, collation=_COLLATION),
        nullable=False,
    )
    is_admin = Column(
        BIT(),
        nullable=False,
    )
    enabled = Column(
        BIT(),
        nullable=False,
    )


class ChatRecord(Base):
    __tablename__ = 'chat'
    id = Column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
    )
    user_id = Column(
        INTEGER(unsigned=True),
        ForeignKey('user.id'),
        nullable=False,
    )


class ErrorsRecord(Base):
    __tablename__ = 'error'
    id = Column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
    )
    error = Column(
        String(500, collation=_COLLATION),
        unique=True,
        nullable=False,
    )


class MessageRecord(Base):
    __tablename__ = 'message'
    id = Column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
    )
    chat_id = Column(
        INTEGER(unsigned=True),
        nullable=False,
    )
    response = Column(
        TEXT(collation=_COLLATION),
        unique=True,
        nullable=True,
    )
    user_input = Column(
        TEXT(collation=_COLLATION),
        unique=True,
        nullable=False,
    )
    model = Column(
        String(15, collation=_COLLATION),
        nullable=False,
    )
    timestamp = Column(
        DateTime, nullable=True
    )

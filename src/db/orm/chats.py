from datetime import datetime

import pytz
from sqlalchemy import Integer, ForeignKey, Text, Boolean, String, DateTime, Enum, PrimaryKeyConstraint, func, \
    UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.enums import ChatType
from db.orm.base import DateTimeMixin, Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from db.orm import User


class Message(DateTimeMixin):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey("chats.id"))
    recipient_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), default=None, nullable=True)
    content: Mapped[str] = mapped_column(Text)

    is_sent: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    delivered_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    read_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    sender: Mapped['User'] = relationship(
        "User",
        back_populates="sent_messages",
        foreign_keys=[sender_id]
    )
    recipient: Mapped['User'] = relationship(
        "User",
        back_populates="received_messages",
        foreign_keys=[recipient_id]
    )
    chat: Mapped['Chat'] = relationship(
        "Chat", back_populates="messages"
    )


class ChatParticipants(Base):
    __tablename__ = "chat_participants"
    __table_args__ = (
        UniqueConstraint("chat_id", "user_id"),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), nullable=False, primary_key=True)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.timezone(
            str(pytz.UTC),
            func.current_timestamp(),
        ),
    )


class Chat(DateTimeMixin):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    is_private: Mapped[bool] = mapped_column(Boolean, default=False)
    about: Mapped[str] = mapped_column(Text, nullable=True)
    type: Mapped[ChatType] = mapped_column(Enum(ChatType), nullable=False)

    participants: Mapped[list['User']] = relationship(
        "User",
        secondary="chat_participants",
        back_populates="chats"
    )
    messages: Mapped[list['Message']] = relationship(
        "Message",
        back_populates="chat"
    )
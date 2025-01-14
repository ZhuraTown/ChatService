from datetime import datetime
from sqlalchemy import Integer, ForeignKey, Text, Boolean, String, DateTime, Enum, PrimaryKeyConstraint
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
    recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
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
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), nullable=False, primary_key=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Chat(DateTimeMixin):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    is_private: Mapped[bool] = mapped_column(Boolean, default=False)
    about: Mapped[str] = mapped_column(Text, nullable=True)
    type_chat: Mapped[ChatType] = mapped_column(Enum(ChatType), nullable=False)

    participants: Mapped[list['User']] = relationship(
        "User",
        secondary="chat_participants",
        back_populates="chats"
    )
    messages: Mapped[list['Message']] = relationship(
        "Message",
        back_populates="chat"
    )
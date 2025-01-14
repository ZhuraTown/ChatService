from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.orm.base import DateTimeMixin
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from db.orm.chats import Chat, Message


class User(DateTimeMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)

    chats: Mapped[list['Chat']] = relationship(
        "Chat",
        secondary="chat_participants",
        back_populates="participants"
    )
    sent_messages: Mapped[list['Message']] = relationship(
        "Message",
        back_populates="sender",
        foreign_keys="Message.sender_id"
    )
    received_messages: Mapped[list['Message']] = relationship(
        "Message", back_populates="recipient", foreign_keys="Message.recipient_id"
    )

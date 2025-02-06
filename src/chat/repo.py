from datetime import datetime
from typing import Optional

from sqlalchemy import select, desc
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import joinedload

from db.filter_sets.chats import ChatsFilterSet, MessageChatsFilterSet
from db.orm import Chat, Message, ChatParticipants, User
from db.repository.create_update_mixin import CreateUpdateMixin
from db.repository.list_mixin import ListMixin
from db.repository.retrieve_mixin import RetrieveMixin


class ChatRepository(
    CreateUpdateMixin[Chat],
    ListMixin[Chat, ChatsFilterSet],
    RetrieveMixin[Chat],
):
    model = Chat
    filter_set = ChatsFilterSet

    async def create_participants(
            self,
            chat_id: int,
            participants: list[int],
            joined_at: datetime
    ):
        joined_at = joined_at if joined_at else datetime.utcnow()
        query = insert(ChatParticipants).values(
            [
                {"chat_id": chat_id, "user_id": user_id, "joined_at": joined_at}
                for user_id in participants
            ]
        ).on_conflict_do_nothing()
        await self.session.execute(query)
        await self.session.flush()

    async def find_participants_by(
            self,
            params: dict
    ) -> list[ChatParticipants]:
        query = select(ChatParticipants)
        filtered_query = self.filter_set(query).filter_query(params)
        results = (await self.session.execute(filtered_query)).unique().scalars().all()
        return results

    async def list_chat_user(
            self,
            user: int
    ) -> list[Chat]:
        subquery = (
            select(ChatParticipants)
            .where(ChatParticipants.user_id == user)
        )
        query = (
            select(Chat)
            .where(Chat.id.in_(subquery), Chat.deleted_at.is_(None))
        )
        results = (await self.session.execute(query)).unique().scalars().all()
        return results

    async def list_participants(
            self,
            chat_id: int
    ) -> list[User]:
        participants_subquery = select(ChatParticipants.user_id).where(ChatParticipants.chat_id == chat_id)
        query = select(User).where(User.id.in_(participants_subquery))
        result = await self.session.scalars(query)
        return result.all()


class MessageRepository(
    CreateUpdateMixin[Message],
):
    model = Message
    filter_set = MessageChatsFilterSet

    async def list_messages(
            self,
            chat_id: int,
            limit: int = 10,
            offset: int = 0,
    ) -> list[Message]:
        messages = await self.session.scalars(
            select(Message)
            .where(Message.chat_id == chat_id)
            .options(
                joinedload(Message.sender)
            ).limit(limit).offset(offset)
            .order_by(desc(Message.created_at))
        )
        return messages.all()

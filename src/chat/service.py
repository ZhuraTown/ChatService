from datetime import datetime
from typing import List, Optional

from chat.repo import ChatRepository
from chat.schemas import CreateChatSchemaRequest, ChatParticipantsFilters
from common.exceptions import UsersNotFound, UserNotBelongChat
from common.uow import SQLAlchemyUoW
from db.filter_sets.chats import ChatParticipantsFilterSet
from db.orm import Chat
from users.repo import UserRepository
from users.schemas import UsersFilters


class ChatService:

    async def _participants_exists(
            self,
            participants: list[int]
    ):
        found_participants = await self.user_repo.list(
            UsersFilters(id__in=participants).model_dump(exclude_none=True)
        )
        if len(found_participants) != len(participants):
            raise UsersNotFound()

    async def _user_belong_participants_chat(
            self, chat_id: int, users: [int]
    ):
        found_participants = await self.chat_repo.find_participants_by(
            ChatParticipantsFilters(user__id__in=users, chat_id=chat_id)
            .model_dump(exclude_none=True)
        )
        if not found_participants:
            raise UserNotBelongChat()

    def __init__(
            self,
            user_repo,
            message_repo,
            chat_repo,
            uow: SQLAlchemyUoW
    ):
        self.user_repo: UserRepository = user_repo
        self.message_repo = message_repo
        self.chat_repo: ChatRepository = chat_repo
        self.uow = uow

    async def _create_participants(
            self,
            chat_id: int,
            participants: list[int],
            chat_created_at: Optional[datetime] = None
    ):
        await self.chat_repo.create_participants(
            chat_id,
            participants,
            chat_created_at
        )

    async def get_chat(
            self,
            oid: int
    ) -> Chat:
        return await self.chat_repo.find_by_id(oid)

    async def create_chat(
            self,
            chat_data: CreateChatSchemaRequest,
            creator: int,
    ) -> Chat:
        await self._participants_exists(chat_data.participants)

        chat_data = chat_data.model_dump(mode='json')
        participants = chat_data.pop('participants', [])
        participants.append(creator)

        new_chat = await self.chat_repo.create(chat_data)
        await self.chat_repo.create_participants(
            new_chat.id,
            participants,
            new_chat.created_at
        )
        await self.uow.commit()
        return new_chat

    async def delete_chat(
            self,
            oid: int,
            remover: int,
    ):

        await self._user_belong_participants_chat(oid, [remover])

    async def add_participants(
            self,
            chat_oid: int,
            user: int,
            participants: list[int]
    ):
        await self._user_belong_participants_chat(chat_oid, [user])

        await self._create_participants(chat_oid, participants)
        await self.uow.commit()

    async def list_chats_user(
            self,
            user_id: int
    ):
        return await self.chat_repo.list_chat_user(user_id)


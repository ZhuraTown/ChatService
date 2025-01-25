from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from chat.repo import ChatRepository
from chat.service import ChatService
from common.uow import SQLAlchemyUoW
from db.dependency import get_session
from users.dependency import get_user_repository
from users.repo import UserRepository


def get_chat_repository(
        session: Annotated[AsyncSession, Depends(get_session)],
):
    return ChatRepository(session)


def get_chat_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    chat_repo: Annotated[ChatRepository, Depends(get_chat_repository)]
) -> ChatService:
    return ChatService(
        user_repo=user_repo,
        chat_repo=chat_repo,
        message_repo=None,
        uow=SQLAlchemyUoW(session=session)
    )

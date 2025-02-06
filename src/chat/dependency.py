from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, Query, WebSocketException, status
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket

from chat.repo import ChatRepository, MessageRepository
from chat.service import ChatService
from common.uow import SQLAlchemyUoW
from config import get_auth_data
from db.dependency import get_session
from db.orm import Chat
from users.dependency import get_user_repository
from users.repo import UserRepository


def get_chat_repository(
        session: Annotated[AsyncSession, Depends(get_session)],
):
    return ChatRepository(session)


def get_message_repository(
        session: Annotated[AsyncSession, Depends(get_session)],
):
    return MessageRepository(session)


def get_chat_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    chat_repo: Annotated[ChatRepository, Depends(get_chat_repository)],
    message_repo: Annotated[MessageRepository, Depends(get_message_repository)],
) -> ChatService:
    return ChatService(
        user_repo=user_repo,
        chat_repo=chat_repo,
        message_repo=message_repo,
        uow=SQLAlchemyUoW(session=session)
    )


async def auth_user(
        websocket: WebSocket,
        user_repo: Annotated[UserRepository, Depends(get_user_repository)],
):
    access_token = websocket.query_params.get("access_token")
    if not access_token:
        await websocket.close(code=1008)
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    try:
        auth_data = get_auth_data()
        payload = jwt.decode(
            access_token,
            auth_data['secret_key'],
            algorithms=auth_data['algorithm']
        )
    except JWTError:
        await websocket.close(code=1008)
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        await websocket.close(code=1008)
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    user_id: str = payload.get('sub')
    if not user_id:
        await websocket.close(code=1008)
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    user = await user_repo.find_by_id(user_id)
    if not user:
        await websocket.close(code=1008)
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return user


async def get_chat(
        chat_id: int,
        chat_service: Annotated[ChatService, Depends(get_chat_service)]
) -> Chat:
    found_chat = await chat_service.get_chat(chat_id)
    if not found_chat:
        raise WebSocketException(code=status.WS_1007_INVALID_FRAME_PAYLOAD_DATA)
    return found_chat

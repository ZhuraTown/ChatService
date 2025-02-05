from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, Query, WebSocketException, status
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket

from chat.repo import ChatRepository
from chat.service import ChatService
from common.uow import SQLAlchemyUoW
from config import get_auth_data
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
        raise WebSocketException(code=1008, reason="Invalid access token")

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        await websocket.close(code=1008)
        raise WebSocketException(code=1008, reason="Invalid access token")

    user_id: str = payload.get('sub')
    if not user_id:
        await websocket.close(code=1008)
        raise WebSocketException(code=1008, reason="Invalid access token")

    user = await user_repo.find_by_id(user_id)
    if not user:
        await websocket.close(code=1008)
        raise WebSocketException(code=1008, reason="Invalid access token")
    return user

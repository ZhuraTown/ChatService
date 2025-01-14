from typing import Annotated

from fastapi import Request, Depends
from jose import jwt, JWTError
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from common.uow import SQLAlchemyUoW
from config import get_auth_data
from common.exceptions import TokenNotValid
from db.dependency import get_session
from users.auth import security
from users.repo import UserRepository
from users.service import UserService


def get_user_repository(
        session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRepository:
    return UserRepository(session)


def get_user_service(
    session: Annotated[AsyncSession, Depends(get_session)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(
        user_repo=user_repo,
        uow=SQLAlchemyUoW(session=session)
    )


async def get_current_user(
        user_repo: Annotated[UserRepository, Depends(get_user_repository)],
        token: str = Depends(security)
):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(
            token.credentials, # noqa
            auth_data['secret_key'],
            algorithms=auth_data['algorithm']
        )
    except JWTError:
        raise TokenNotValid()

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenNotValid()

    user_id: str = payload.get('sub')
    if not user_id:
        raise TokenNotValid()

    user = await user_repo.find_by_id(user_id)
    if not user:
        raise TokenNotValid()
    return user

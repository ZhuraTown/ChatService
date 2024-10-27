from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_session
from src.users.repository import UserRepository
from src.users.service import UserService


def get_user_service(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> UserService:
    return UserService(
        user_repository=UserRepository(),
        session=session
    )
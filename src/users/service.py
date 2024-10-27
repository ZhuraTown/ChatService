from sqlalchemy.ext.asyncio import AsyncSession

from src.users.interface import UserRepositoryI
from src.users.models import *


class UserService:

    def __init__(
            self,
            user_repository,
            session: AsyncSession,
    ):
        self._user_repository: UserRepositoryI = user_repository
        self._session = session

    async def create(
            self,
            user: UserCreate
    ) -> UserRead:
        # todo: add validation for unique username
        # todo: add hash password
        return await self._user_repository.create(self._session, user)

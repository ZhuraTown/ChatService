from typing import Protocol
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import UserCreate, UserRead


class UserRepositoryI:

    async def create(self, session: AsyncSession, user: UserCreate) -> UserRead: ...

    async def get(self, session: AsyncSession, oid: UUID) -> UserRead: ...

    async def list(self, session: AsyncSession) -> list[UserRead]: ...

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.users.models import UserCreate, UserRead, User


class UserRepository:

    async def create(self, session: AsyncSession, user: UserCreate) -> UserRead:
        try:
            db_user = User.model_validate(user)
            session.add(db_user)
            await session.flush()
            return user
        except Exception as ex:
            await session.rollback()
            raise ex

    async def get(self, session: AsyncSession, oid: UUID) -> UserRead:
        user = await session.execute(select(User).where(User.oid == oid))
        return user

    async def list(self, session: AsyncSession) -> list[UserRead]:
        ...

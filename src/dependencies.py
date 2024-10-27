from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import db


async def get_session() -> AsyncSession:
    async with db.session() as session:
        yield session

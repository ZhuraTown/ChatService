from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

from src.db.engine import engine


class Database:
    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[type[AsyncSession], None]:
        async with self.session_factory() as session:
            try:
                yield session
            except Exception as ex:
                print(f"Error{ex}")
                await session.rollback()
            finally:
                await session.commit()
                await session.close()


db = Database(engine=engine)

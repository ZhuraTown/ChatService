from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings

engine = create_async_engine(
    URL.create(
        drivername="postgresql+asyncpg",
        username=settings.infrastructure.db_user,
        password=settings.infrastructure.db_password,
        host=settings.infrastructure.db_host,
        port=settings.infrastructure.db_port,
        database=settings.infrastructure.db_name,
    ),
    echo=True if settings.debug else False,
)


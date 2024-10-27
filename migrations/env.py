import asyncio
from logging.config import fileConfig

from sqlalchemy import engine_from_config, Connection
from sqlalchemy import pool, URL
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlmodel import SQLModel
from migrations import tables

from alembic import context

from src.config import settings

config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = SQLModel.metadata

url_connect = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.infrastructure.db_user,
    password=settings.infrastructure.db_password,
    host=settings.infrastructure.db_host,
    port=settings.infrastructure.db_port,
    database=settings.infrastructure.db_name,
)


def run_migrations_offline() -> None:
    context.configure(
        url=url_connect,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    configurations = config.get_section(config.config_ini_section, {})
    configurations['sqlalchemy.url'] = url_connect
    connectable = async_engine_from_config(
        configurations,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
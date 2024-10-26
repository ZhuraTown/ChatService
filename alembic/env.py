from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool, URL

from alembic import context

from src.config import settings

config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = None

url_connect = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.infrastructure.user,
    password=settings.infrastructure.password,
    host=settings.infrastructure.host,
    port=settings.infrastructure.port,
    database=settings.infrastructure.name,
)


def run_migrations_offline() -> None:
    url = url_connect
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

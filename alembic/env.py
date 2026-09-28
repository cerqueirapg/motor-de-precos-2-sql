import asyncio
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Adiciona o diretório raiz do projeto ao sys.path para garantir imports absolutos de 'app'
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Importa todos os modelos de DB para garantir que estejam registrados nos metadados do Alembic
import app.models.db_models  # noqa: F401
from app.core.config import settings
from app.core.database import Base

config = context.config

# Sobrescrever a URL do alembic.ini com a URL assíncrona definida nas configurações da app
if hasattr(settings, "DATABASE_URL") and settings.DATABASE_URL:
    config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name:
    fileConfig(config.config_file_name)

# Mapear os metadados dos seus modelos ORM
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Executa migrações no modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Executa migrações no modo 'online' utilizando Engine Assíncrono."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Executa migrações no modo 'online'."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

# Para SQLite em desenvolvimento/testes (requer o pacote `aiosqlite`)
# Para PostgreSQL em produção, utilize: "postgresql+asyncpg://user:pass@localhost:5432/dbname"
DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"

# Engine assíncrono
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Exibe no terminal os SQLs gerados (útil para depuração)
)

# Fábrica de sessões assíncronas
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Classe Base para mapeamento das tabelas
class Base(DeclarativeBase):
    pass


# Dependência do FastAPI para injeção de sessão nas rotas
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

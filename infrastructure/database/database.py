from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

from .models import Base

def create_engine(url) -> AsyncEngine:
    return create_async_engine(url, echo=False) # флаг echo для подробных логов

def create_async_session_factory(engine) -> sessionmaker:
    return sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

async def drop_database(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def create_database(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
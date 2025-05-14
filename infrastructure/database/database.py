from sqlalchemy import MetaData
from core.config import DatabaseConfig
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
)
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, config: DatabaseConfig):
        self.engine = self._create_engine(config)
        self.session_factory = self._create_session_factory()

    def _create_engine(self, config: DatabaseConfig) -> AsyncEngine:
        return create_async_engine(
            config.database_url, echo=False
        )  # флаг echo для подробных логов

    def _create_session_factory(self) -> sessionmaker:
        return sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    def get_engine(self) -> AsyncEngine:
        return self.engine

    def get_session_factory(self) -> sessionmaker:
        return self.session_factory

    async def create_database(self, metadata: MetaData) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(metadata.create_all)

    async def drop_database(self, metadata: MetaData) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(metadata.drop_all)

    async def shutdown(self) -> None:
        if self.engine:
            await self.engine.dispose()

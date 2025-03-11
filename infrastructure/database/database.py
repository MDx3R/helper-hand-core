from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

from .models import Base

def create_engine(url) -> AsyncEngine:
    return create_async_engine(url, echo=True)

def create_async_session_factory(engine) -> sessionmaker:
    return sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

def create_database(engine) -> None:
    Base.metadata.create_all(engine)
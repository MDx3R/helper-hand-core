from contextvars import ContextVar
from contextlib import asynccontextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

import sqlalchemy.exc
import psycopg2
import re

from domain.exceptions import ApplicationException, RepositoryException
from domain.exceptions.repository import IntegrityException, DuplicateEntryException

from application.transactions import TransactionManager

from infrastructure.exceptions.database import (
    DatabaseUnavailableException,
    InvalidQueryException,
    InvalidDataException, 
    InvalidStatementException
)

current_session: ContextVar[AsyncSession] = ContextVar("current_session", default=None)

class SQLAlchemyTransactionManager(TransactionManager):
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory

    def _create_session(self) -> AsyncSession:
        return self.session_factory()

    def _get_session(self) -> AsyncSession | None:
        return current_session.get()

    def _set_session(self, session: AsyncSession):
        current_session.set(session)

    def _drop_session(self):
        current_session.set(None)

    async def _rollback(self, session: AsyncSession):
        await session.rollback()

    async def _commit(self, session: AsyncSession):
        await session.commit()

    async def _close(self, session: AsyncSession):
        await session.close()

    def _extract_duplicate_info(self, error) -> tuple[str, str]:
        match = re.search(r'\((\w+)\)=\((.*?)\)', str(error))
        if match:
            return match.group(1), match.group(2)
        return "unknown_field", "unknown_value"

    def _handle_exception(self, exception):
        if isinstance(exception, ApplicationException):
            raise exception
        
        if isinstance(exception, sqlalchemy.exc.IntegrityError):
            if isinstance(exception.orig, psycopg2.errors.UniqueViolation):
                field, value = self._extract_duplicate_info(exception.orig)
                raise DuplicateEntryException(field, value) from exception
            raise IntegrityException from exception
        
        if isinstance(exception, sqlalchemy.exc.OperationalError):
            raise DatabaseUnavailableException from exception

        if isinstance(exception, sqlalchemy.exc.ProgrammingError):
            raise InvalidQueryException from exception

        if isinstance(exception, sqlalchemy.exc.DataError):
            raise InvalidDataException from exception

        if isinstance(exception, sqlalchemy.exc.StatementError):
            raise InvalidStatementException from exception

        if isinstance(exception, sqlalchemy.exc.SQLAlchemyError):
            raise RepositoryException from exception
        
        raise exception

    async def __aenter__(self):
        session = self._create_session()
        self._set_session(session)
        return session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        session = self._get_session()

        if not session:
            return

        is_raised = exc_type is not None

        try:
            if not is_raised:
                await self._commit(session)
            else:
                await self._rollback(session)
        finally:
            await self._close(session)
            self._drop_session()

        if is_raised:
            self._handle_exception(exc_val)

    @asynccontextmanager
    async def get_session(self):
        """
        Контекстный менеджер для получения сессии.
        - Если транзакция активна, используем существующую сессию.
        - Если транзакции нет, создаём временную сессию, используем и закрываем.
        """
        session = self._get_session()
        if session is not None:
            yield session # Используем существующую сессию
        else:
            session = self._create_session()
            try:
                yield session # Временная сессия. Закрывается автоматически
                await self._commit(session)
            except Exception as e:
                await self._rollback(session)
                self._handle_exception(e)
            finally:
                await self._close(session) # todo: также поместить в try-catch, чтобы исключения ORM не поднимались.
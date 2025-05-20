import asyncio
from asyncpg import InterfaceError
import pytest
import pytest_asyncio

from application.transactions.configuration import set_transaction_manager
from application.transactions.transaction_manager import TransactionManager
from application.transactions.transactional import transactional
from domain.dto.user.internal.user_filter_dto import ContractorFilterDTO
from domain.repositories.user.contractor.contractor_command_repository import (
    ContractorCommandRepository,
)
from domain.repositories.user.contractor.contractor_query_repository import (
    ContractorQueryRepository,
)
from infrastructure.database.database import Database
from infrastructure.database.models import Base
from infrastructure.repositories.base import QueryExecutor
from infrastructure.repositories.user.contractor.contractor_command_repository import (
    ContractorCommandRepositoryImpl,
)
from infrastructure.repositories.user.contractor.contractor_query_repository import (
    ContractorQueryRepositoryImpl,
)
from infrastructure.transactions.transaction_manager import (
    SQLAlchemyTransactionManager,
    current_session,
)
from domain.entities.user.contractor.contractor import Contractor
from tests.data_generators import ContractorDataGenerator
from tests.factories import ContractorFactory


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db(database: Database):
    meta = Base.metadata
    await database.drop_database(meta)
    await database.create_database(meta)
    yield
    await asyncio.sleep(0.1)
    try:
        await database.drop_database(meta)
    except InterfaceError:
        print("WARNING: DB drop failed due to pending operation (ignored)")


@pytest.fixture(scope="session")
def session_factory(database: Database):
    return database.get_session_factory()


@pytest.fixture(scope="session")
def transaction_manager(session_factory):
    manager = SQLAlchemyTransactionManager(session_factory)
    set_transaction_manager(manager)
    return manager


@pytest.fixture(scope="session")
def query_executor(transaction_manager):
    return QueryExecutor(transaction_manager)


@pytest.fixture()
def user_command_repository(query_executor: QueryExecutor):
    return ContractorCommandRepositoryImpl(query_executor)


@pytest.fixture()
def user_query_repository(query_executor: QueryExecutor):
    return ContractorQueryRepositoryImpl(query_executor)


class TestTransactionManagerImpl:
    """Тестовый набор для класса SQLAlchemyTransactionManager."""

    @pytest.fixture(autouse=True)
    def setup(
        self,
        user_command_repository: ContractorCommandRepository,
        user_query_repository: ContractorQueryRepository,
        transaction_manager: TransactionManager,
    ):
        self.user_command_repository = user_command_repository
        self.user_query_repository = user_query_repository
        self.transaction_manager = transaction_manager

    def _get_user(self) -> Contractor:
        gen = ContractorDataGenerator()
        factory = ContractorFactory(gen)
        return factory.create_default()

    async def _is_user_saved(self, user: Contractor) -> bool:
        result = await self.user_query_repository.filter_contractors(
            ContractorFilterDTO(phone_number=user.phone_number)
        )
        return user.phone_number in [i.phone_number for i in result]

    async def _create_user(self, user: Contractor) -> Contractor:
        return await self.user_command_repository.create_contractor(user)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_transaction_commit(self):
        contractor = self._get_user()
        async with self.transaction_manager as session:
            result = await self._create_user(contractor)

        assert result is not None
        assert result.name == contractor.name
        assert await self._is_user_saved(contractor)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_transaction_rollback(self):
        contractor = self._get_user()
        with pytest.raises(ValueError, match="Test rollback"):
            async with self.transaction_manager as session:
                await self._create_user(contractor)
                raise ValueError("Test rollback")

        assert not await self._is_user_saved(contractor)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_nested_transaction_is_shared(self):
        async with self.transaction_manager as outer_session:
            async with self.transaction_manager as inner_session:
                assert id(outer_session) == id(inner_session)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_consecutive_transactions_not_shared(self):
        first_session = None
        async with self.transaction_manager as session:
            first_session = session

        second_session = None
        async with self.transaction_manager as session:
            second_session = session

        assert id(first_session) != id(second_session)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_session_cleared_on_commit(self):
        async with self.transaction_manager as session:
            assert current_session.get() is not None

        assert current_session.get() is None

    @pytest.mark.asyncio(loop_scope="session")
    async def test_session_cleared_on_rollback(self):
        with pytest.raises(ValueError, match="Test rollback"):
            async with self.transaction_manager as session:
                assert current_session.get() is not None
                raise ValueError("Test rollback")

        assert current_session.get() is None

    @pytest.mark.asyncio(loop_scope="session")
    async def test_transactional_commit(self):
        contractor = self._get_user()

        @transactional
        async def func(self):
            return await self._create_user(contractor)

        result = await func(self)
        assert result is not None
        assert result.name == contractor.name
        assert await self._is_user_saved(contractor)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_transactional_rollback(self):
        contractor = self._get_user()

        @transactional
        async def func(self):
            await self._create_user(contractor)
            raise ValueError("Test rollback")

        with pytest.raises(ValueError, match="Test rollback"):
            await func(self)
        assert not await self._is_user_saved(contractor)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_transactional_creates_session(self):
        @transactional
        async def func(self):
            assert current_session.get() is not None

        await func(self)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_transactional_shares_transaction(self):
        @transactional
        async def func(self):
            outer_session = current_session.get()
            async with self.transaction_manager as inner_session:
                assert id(outer_session) == id(inner_session)

        await func(self)

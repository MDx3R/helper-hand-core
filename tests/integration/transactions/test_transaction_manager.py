import pytest
import pytest_asyncio
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.models import Base
from infrastructure.database.database import create_async_session_factory, create_engine, create_database, drop_database
from infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from infrastructure.transactions.transaction_manager import SQLAlchemyTransactionManager
from domain.entities import Contractee, Contractor
from domain.entities.enums import RoleEnum, UserStatusEnum, GenderEnum, PositionEnum, CitizenshipEnum
from application.transactions import TransactionManager
from domain.repositories import UserRepository

DB_URL = "postgresql+asyncpg://postgres:246224682@localhost:5432/test_db"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def engine():
    return create_engine(DB_URL)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db(engine):
    await drop_database(engine)
    await create_database(engine)
    yield
    await drop_database(engine)

@pytest.fixture(scope="session")
def session_factory(engine):
    return create_async_session_factory(engine)

@pytest.fixture()
def transaction_manager(session_factory):
    return SQLAlchemyTransactionManager(session_factory)

@pytest.fixture()
def user_repository(transaction_manager):
    return SQLAlchemyUserRepository(transaction_manager)

@pytest.mark.asyncio(scope="session")
async def test_transaction_commit(user_repository: UserRepository, transaction_manager: TransactionManager):
    async with transaction_manager as session:
        contractee = Contractee(
            surname="Doe", name="John", patronymic=None,
            phone_number="1234567890", role=RoleEnum.contractee,
            status=UserStatusEnum.pending, photos=[],
            telegram_id=12345, chat_id=67890,
            birthday="2000-01-01", height=180, gender=GenderEnum.male,
            citizenship=CitizenshipEnum.russia, positions=[PositionEnum.hostess]
        )
        await user_repository.save_contractee(contractee)
    
    result = await user_repository.get_contractee(contractee.contractee_id)
    assert result is not None
    assert result.name == "John"

@pytest.mark.asyncio(scope="session")
async def test_transaction_rollback(user_repository: UserRepository, transaction_manager: TransactionManager):
    with pytest.raises(ValueError, match="Test rollback"):
        async with transaction_manager as session:
            contractor = Contractor(
                surname="Doe", name="Jane", patronymic=None,
                phone_number="9876543210", role=RoleEnum.contractor,
                status=UserStatusEnum.pending, photos=[],
                telegram_id=54321, chat_id=98765,
                about="Company XYZ"
            )
            await user_repository.save_contractor(contractor)
            raise ValueError("Test rollback")
    
    result = await user_repository.get_contractor(contractor.contractor_id)
    assert result is None

@pytest.mark.asyncio(scope="session")
async def test_transaction_session_is_shared(user_repository: UserRepository, transaction_manager: TransactionManager):
    async with transaction_manager as session:
        contractee = Contractee(
            surname="Smith", name="Alice", patronymic=None,
            phone_number="111222333", role=RoleEnum.contractee,
            status=UserStatusEnum.pending, photos=[],
            telegram_id=13579, chat_id=24680,
            birthday="1995-06-15", height=170, gender=GenderEnum.female,
            citizenship=CitizenshipEnum.russia, positions=[PositionEnum.helper]
        )
        await user_repository.save_contractee(contractee)
        
        contractor = Contractor(
            surname="Smith", name="Bob", patronymic=None,
            phone_number="444555666", role=RoleEnum.contractor,
            status=UserStatusEnum.pending, photos=[],
            telegram_id=98765, chat_id=43210,
            about="Business Owner"
        )
        await user_repository.save_contractor(contractor)
        
        session_id_1 = id(session)
        session_id_2 = id(await transaction_manager.get_session().__aenter__())
    
    assert session_id_1 == session_id_2

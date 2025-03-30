import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime
from contextlib import asynccontextmanager

from domain.entities import User, Admin, Contractee, Contractor
from domain.entities.enums import RoleEnum, UserStatusEnum, GenderEnum, CitizenshipEnum, PositionEnum
from infrastructure.database.models import UserBase, AdminBase, ContracteeBase, ContractorBase
from infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from application.transactions import TransactionManager

@pytest.fixture
def transaction_manager_mock():
    mock = AsyncMock(spec=TransactionManager)
    
    session_mock = AsyncMock(spec=AsyncSession)

    mock.get_session = MagicMock()
    mock.get_session.return_value.__aenter__ = AsyncMock(return_value=session_mock)
    mock.get_session.return_value.__aexit__ = AsyncMock(return_value=None)

    return mock

@pytest.fixture
def user_repository(transaction_manager_mock):
    return SQLAlchemyUserRepository(transaction_manager_mock)

@pytest.mark.parametrize(
    "user_id, expected_result",
    [
        (1, UserBase(user_id=1, surname="Ivanov", name="Ivan", phone_number="+79123456789", role=RoleEnum.contractee, status=UserStatusEnum.pending, telegram_id=12345, chat_id=67890, photos=[])),  # Существующий пользователь
        (999, None),  # Несуществующий пользователь
    ],
)
@pytest.mark.asyncio
async def test_get_user(user_id, expected_result, user_repository, transaction_manager_mock):
    session_mock = transaction_manager_mock.get_session.return_value.__aenter__.return_value
    session_mock.execute.return_value = MagicMock(scalar_one_or_none=MagicMock(return_value=expected_result))

    result = await user_repository.get_user(user_id)

    if expected_result is None:
        assert result is None
    else:
        assert result is not None
        assert result.user_id == expected_result.user_id
        assert result.surname == expected_result.surname
        assert result.name == expected_result.name
        assert result.phone_number == expected_result.phone_number
        assert result.role == expected_result.role
        assert result.status == expected_result.status
        assert result.telegram_id == expected_result.telegram_id
        assert result.chat_id == expected_result.chat_id
        assert result.photos == expected_result.photos

@pytest.mark.asyncio
async def test_get_user_by_telegram_id(user_repository, transaction_manager_mock):
    telegram_id = 12345
    user_base = UserBase(user_id=1, surname="Ivanov", name="Ivan", phone_number="+79123456789", role=RoleEnum.contractee, status=UserStatusEnum.pending, telegram_id=telegram_id, chat_id=67890, photos=[])
    
    session_mock = transaction_manager_mock.get_session.return_value.__aenter__.return_value
    session_mock.execute.return_value = MagicMock(scalar_one_or_none=MagicMock(return_value=user_base))

    result = await user_repository.get_user_by_telegram_id(telegram_id)

    assert result is not None
    assert result.telegram_id == telegram_id

@pytest.mark.asyncio
async def test_get_admin(user_repository, transaction_manager_mock):
    admin_id = 1
    user_base = UserBase(user_id=admin_id, surname="Ivanov", name="Ivan", phone_number="+79123456789", role=RoleEnum.admin, status=UserStatusEnum.pending, telegram_id=12345, chat_id=67890, photos=[])
    admin_base = AdminBase(admin_id=admin_id, about="Admin info")
    
    session_mock = transaction_manager_mock.get_session.return_value.__aenter__.return_value
    session_mock.execute.return_value = MagicMock(first=MagicMock(return_value=(user_base, admin_base)))

    result = await user_repository.get_admin(admin_id)

    assert result is not None
    assert result.user_id == admin_id
    assert result.role == RoleEnum.admin
    assert result.about == "Admin info"

@pytest.mark.asyncio
async def test_get_contractee(user_repository, transaction_manager_mock):
    contractee_id = 1
    user_base = UserBase(user_id=contractee_id, surname="Ivanov", name="Ivan", phone_number="+79123456789", role=RoleEnum.contractee, status=UserStatusEnum.pending, telegram_id=12345, chat_id=67890, photos=[])
    contractee_base = ContracteeBase(contractee_id=contractee_id, birthday=datetime(1990, 1, 1), height=180, gender=GenderEnum.male, citizenship=CitizenshipEnum.russia, positions=[PositionEnum.helper])
    
    session_mock = transaction_manager_mock.get_session.return_value.__aenter__.return_value
    session_mock.execute.return_value = MagicMock(first=MagicMock(return_value=(user_base, contractee_base)))

    result = await user_repository.get_contractee(contractee_id)

    assert result is not None
    assert result.user_id == contractee_id
    assert result.role == RoleEnum.contractee
    assert result.birthday == datetime(1990, 1, 1)
    assert result.height == 180
    assert result.gender == GenderEnum.male
    assert result.citizenship == CitizenshipEnum.russia
    assert result.positions == [PositionEnum.helper]

@pytest.mark.asyncio
async def test_get_contractor(user_repository, transaction_manager_mock):
    contractor_id = 1
    user_base = UserBase(user_id=contractor_id, surname="Ivanov", name="Ivan", phone_number="+79123456789", role=RoleEnum.contractor, status=UserStatusEnum.pending, telegram_id=12345, chat_id=67890, photos=[])
    contractor_base = ContractorBase(contractor_id=contractor_id, about="Contractor info")
    
    session_mock = transaction_manager_mock.get_session.return_value.__aenter__.return_value
    session_mock.execute.return_value = MagicMock(first=MagicMock(return_value=(user_base, contractor_base)))

    result = await user_repository.get_contractor(contractor_id)

    assert result is not None
    assert result.user_id == contractor_id
    assert result.role == RoleEnum.contractor
    assert result.about == "Contractor info"

@pytest.mark.asyncio
async def test_get_admins(user_repository, transaction_manager_mock):
    user_base_1 = UserBase(
        user_id=1,
        surname="Ivanov",
        name="Ivan",
        phone_number="+79123456789",
        role=RoleEnum.admin,
        status=UserStatusEnum.registered,
        telegram_id=12345,
        chat_id=67890,
        photos=[]
    )
    admin_base_1 = AdminBase(admin_id=1, about="Admin 1 info")

    user_base_2 = UserBase(
        user_id=2,
        surname="Petrov",
        name="Petr",
        phone_number="+79223456789",
        role=RoleEnum.admin,
        status=UserStatusEnum.registered,
        telegram_id=54321,
        chat_id=98765,
        photos=[]
    )
    admin_base_2 = AdminBase(admin_id=2, about="Admin 2 info")

    session_mock = transaction_manager_mock.get_session.return_value.__aenter__.return_value
    mock_result = MagicMock()
    mock_result.all.return_value = [
        (user_base_1, admin_base_1),
        (user_base_2, admin_base_2)
    ]
    session_mock.execute.return_value = mock_result

    admins = await user_repository.get_admins()
    
    assert len(admins) == 2

@pytest.mark.parametrize(
    "user_id",
    [
        None,  # Без user_id, должен вызываться _insert_user
        1,     # С user_id, должен вызываться _merge_user
    ],
)
@pytest.mark.asyncio
async def test_save_contractee(user_id, user_repository, transaction_manager_mock):
    contractee = Contractee(
        user_id=user_id,  # Передаем user_id (или None)
        surname="Ivanov",
        name="Ivan",
        phone_number="+79123456789",
        role=RoleEnum.contractee,
        telegram_id=12345,
        chat_id=67890,
        status=UserStatusEnum.pending,
        photos=[],
        birthday=datetime(1990, 1, 1),
        height=180,
        gender=GenderEnum.male,
        citizenship=CitizenshipEnum.russia,
        positions=[PositionEnum.helper]
    )
    
    session_mock = transaction_manager_mock.get_session.return_value.__aenter__.return_value

    def mock_add(entity):
        # Эмулируем назначение user_id
        if isinstance(entity, UserBase):
            entity.user_id = 1  # Назначаем user_id

    session_mock.add.side_effect = mock_add
    
    def mock_merge(entity):
        if isinstance(entity, UserBase):
            entity.user_id = user_id  # Возвращаем тот же user_id

    session_mock.merge.side_effect = mock_merge

    session_mock.flush = AsyncMock()

    result = await user_repository.save_contractee(contractee)

    assert result is not None
    if user_id is None:
        assert result.user_id == 1  # Проверяем, что user_id был назначен
    else:
        assert result.user_id == user_id  # Проверяем, что user_id остался тем же
    assert result.surname == "Ivanov"
    assert result.name == "Ivan"
    assert result.phone_number == "+79123456789"
    assert result.role == RoleEnum.contractee
    assert result.status == UserStatusEnum.pending
    assert result.telegram_id == 12345
    assert result.chat_id == 67890
    assert result.photos == []
    assert result.birthday == datetime(1990, 1, 1)
    assert result.height == 180
    assert result.gender == GenderEnum.male
    assert result.citizenship == CitizenshipEnum.russia
    assert result.positions == [PositionEnum.helper]

    # Проверяем, что session.flush был вызван
    session_mock.flush.assert_awaited()

@pytest.mark.parametrize(
    "user_id",
    [
        None,  # Без user_id, должен вызываться _insert_user
        1,     # С user_id, должен вызываться _merge_user
    ],
)
@pytest.mark.asyncio
async def test_save_contractor(user_id, user_repository, transaction_manager_mock):
    contractor = Contractor(
        user_id=user_id,  # Передаем user_id (или None)
        surname="Ivanov",
        name="Ivan",
        phone_number="+79123456789",
        role=RoleEnum.contractor,
        telegram_id=12345,
        chat_id=67890,
        status=UserStatusEnum.pending,
        photos=[],
        about="Contractor info"
    )
    
    session_mock = transaction_manager_mock.get_session.return_value.__aenter__.return_value
    
    def mock_add(entity):
        # Эмулируем назначение user_id
        if isinstance(entity, UserBase):
            entity.user_id = 1  # Назначаем user_id

    session_mock.add.side_effect = mock_add

    def mock_merge(entity):
        if isinstance(entity, UserBase):
            entity.user_id = user_id  # Возвращаем тот же user_id

    session_mock.merge.side_effect = mock_merge

    session_mock.flush = AsyncMock()

    result = await user_repository.save_contractor(contractor)

    assert result is not None
    assert result.user_id == 1
    assert result.surname == "Ivanov"
    assert result.name == "Ivan"
    assert result.phone_number == "+79123456789"
    assert result.role == RoleEnum.contractor
    assert result.status == UserStatusEnum.pending
    assert result.telegram_id == 12345
    assert result.chat_id == 67890
    assert result.photos == []
    assert result.about == "Contractor info"

    # Проверяем, что session.flush был вызван
    session_mock.flush.assert_awaited()

@pytest.mark.asyncio
async def test_user_exists_by_phone_number(user_repository, transaction_manager_mock):
    phone_number = "+79123456789"
    
    session_mock = transaction_manager_mock.get_session.return_value.__aenter__.return_value
    session_mock.execute.return_value = MagicMock(scalar=MagicMock(return_value=True))

    result = await user_repository.user_exists_by_phone_number(phone_number)

    assert result is True
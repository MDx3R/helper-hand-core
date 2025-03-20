import pytest
from unittest.mock import AsyncMock, Mock
from datetime import datetime
from application.dtos.input import ContracteeInputDTO
from application.dtos.output import ContracteeOutputDTO
from domain.entities import Contractee
from domain.entities.enums import GenderEnum, CitizenshipEnum, PositionEnum, UserStatusEnum
from domain.services.registration import ContracteeRegistrationService
from domain.exceptions.service import UserBlockedException, AlreadyAuthenticatedException

# Дата-сет для успешной регистрации
successful_registration_data = [
    {
        "surname": "Ivanov",
        "name": "Ivan",
        "phone_number": "+79123456789",
        "telegram_id": 12345,
        "chat_id": 67890,
        "birthday": datetime(1990, 1, 1),
        "height": 180,
        "gender": GenderEnum.male,
        "citizenship": CitizenshipEnum.russia,
        "positions": [PositionEnum.helper],
        "photos": []
    },
    {
        "surname": "Petrov",
        "name": "Petr",
        "phone_number": "+79223456789",
        "telegram_id": 54321,
        "chat_id": 98765,
        "birthday": datetime(1985, 5, 15),
        "height": 170,
        "gender": GenderEnum.female,
        "citizenship": CitizenshipEnum.other,
        "positions": [PositionEnum.hostess],
        "photos": ["photo_url"]
    }
]

# Дата-сет для заблокированного пользователя
blocked_user_data = [
    {
        "surname": "Ivanov",
        "name": "Ivan",
        "phone_number": "+79123456789",
        "telegram_id": 12345,
        "chat_id": 67890,
        "birthday": datetime(1990, 1, 1),
        "height": 180,
        "gender": GenderEnum.male,
        "citizenship": CitizenshipEnum.russia,
        "positions": [PositionEnum.helper],
        "photos": [],
        "status": UserStatusEnum.banned
    }
]

# Дата-сет для уже зарегистрированного пользователя
already_authenticated_user_data = [
    {
        "surname": "Ivanov",
        "name": "Ivan",
        "phone_number": "+79123456789",
        "telegram_id": 12345,
        "chat_id": 67890,
        "birthday": datetime(1990, 1, 1),
        "height": 180,
        "gender": GenderEnum.male,
        "citizenship": CitizenshipEnum.russia,
        "positions": [PositionEnum.helper],
        "photos": [],
        "status": UserStatusEnum.registered
    }
]

counter = 0

# Фикстура для мок-репозитория
@pytest.fixture
def user_repository_mock():
    mock = AsyncMock()

    # Используем side_effect для динамического возврата объекта
    async def save_contractee(contractee: Contractee) -> Contractee:
        global counter
        counter +=1
        return Contractee(
            contractee_id=counter,
            surname=contractee.surname,
            name=contractee.name,
            phone_number=contractee.phone_number,
            role=contractee.role,
            photos=contractee.photos,
            telegram_id=contractee.telegram_id,
            chat_id=contractee.chat_id,
            birthday=contractee.birthday,
            height=contractee.height,
            gender=contractee.gender,
            citizenship=contractee.citizenship,
            positions=contractee.positions
        )

    mock.save_contractee.side_effect = save_contractee
    mock.get_user_by_telegram_id.return_value = None  # По умолчанию пользователь не найден
    return mock

# Фикстура для мок-менеджера транзакций
@pytest.fixture
def transaction_manager_mock():
    mock = AsyncMock()
    # Мок для контекстного менеджера (async with)
    mock.__aenter__ = AsyncMock(return_value=None)
    mock.__aexit__ = AsyncMock(return_value=None)
    return mock

# Фикстура для мок-сервиса уведомлений
@pytest.fixture
def notification_service_mock():
    mock = AsyncMock()
    mock.send_new_contractee_registration_notification = AsyncMock(return_value=None)
    return mock

# Фикстура для сервиса
@pytest.fixture
def contractee_service(user_repository_mock, transaction_manager_mock, notification_service_mock):
    from application.services.registration import ContracteeRegistrationServiceImpl
    service = ContracteeRegistrationServiceImpl(
        user_repository=user_repository_mock,
        transaction_manager=transaction_manager_mock,
        notification_service=notification_service_mock
    )
    return service

# Тест успешной регистрации
@pytest.mark.asyncio
@pytest.mark.parametrize("input_data", successful_registration_data)
async def test_register_contractee_success(input_data, contractee_service: ContracteeRegistrationService, user_repository_mock, transaction_manager_mock, notification_service_mock):
    input_dto = ContracteeInputDTO(**input_data)

    result = await contractee_service.register_user(input_dto)

    # Проверка результата
    assert isinstance(result, ContracteeOutputDTO)
    assert result.contractee_id == counter

    # Проверка вызовов репозитория
    user_repository_mock.get_user_by_telegram_id.assert_awaited_once_with(input_data["telegram_id"])
    user_repository_mock.save_contractee.assert_awaited_once()

    # Проверка вызова уведомления
    notification_service_mock.send_new_contractee_registration_notification.assert_awaited_once()

    # Проверка вызова транзакции
    transaction_manager_mock.__aenter__.assert_awaited_once()
    transaction_manager_mock.__aexit__.assert_awaited_once()

# Тест на блокировку пользователя
@pytest.mark.asyncio
@pytest.mark.parametrize("input_data", blocked_user_data)
async def test_register_blocked_user(input_data, contractee_service: ContracteeRegistrationService, user_repository_mock):
    # Мок для заблокированного пользователя
    user_repository_mock.get_user_by_telegram_id.return_value = Contractee(**input_data)

    with pytest.raises(UserBlockedException):
        input_dto = ContracteeInputDTO(**input_data)
        await contractee_service.register_user(input_dto)

    # Проверка, что сохранение не вызывалось
    user_repository_mock.save_contractee.assert_not_awaited()

# Тест на уже зарегистрированного пользователя
@pytest.mark.asyncio
@pytest.mark.parametrize("input_data", already_authenticated_user_data)
async def test_register_already_authenticated_user(input_data, contractee_service: ContracteeRegistrationService, user_repository_mock):
    # Мок для уже зарегистрированного пользователя
    user_repository_mock.get_user_by_telegram_id.return_value = Contractee(**input_data)

    with pytest.raises(AlreadyAuthenticatedException):
        input_dto = ContracteeInputDTO(**input_data)
        await contractee_service.register_user(input_dto)

    # Проверка, что сохранение не вызывалось
    user_repository_mock.save_contractee.assert_not_awaited()
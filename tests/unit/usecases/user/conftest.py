import pytest
from unittest.mock import AsyncMock

from domain.entities import Contractee, Contractor, Admin, TelegramUser
from domain.entities.enums import RoleEnum

counter = 1

@pytest.fixture
def user_repository():
    mock = AsyncMock()

    async def save(user: Contractee | Contractor | Admin) -> Contractee | Contractor | Admin:
        data = user.get_fields()
        if not user.user_id:
            global counter

            mapper = {
                RoleEnum.contractee: "contractee_id",
                RoleEnum.contractor: "contractor_id",
                RoleEnum.admin: "admin_id",
            }
            role_id_field = mapper.get(user.role)
            data = data | {
                "user_id": counter, 
                role_id_field: counter
            }
        
            counter +=1

        return user.model_validate(data)
        
    async def save_telegram_user(user: TelegramUser) -> TelegramUser:
        return user

    mock.save.side_effect = save
    mock.save_telegram_user.side_effect = save_telegram_user
    return mock

def set_up_counter(user_id: int):
    global counter
    counter = user_id
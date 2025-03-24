from typing import Optional

from domain.entities import User 
from domain.entities.enums import RoleEnum, UserStatusEnum
from domain.dto.base import ApplicationDTO

class UserContextDTO(ApplicationDTO):
    user_id: int
    role: RoleEnum 
    status: UserStatusEnum

    phone_number: str
    telegram_id: int 
    chat_id: int
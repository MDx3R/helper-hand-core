from typing import Optional, List

from domain.entities import User 
from domain.entities.enums import RoleEnum, UserStatusEnum
from domain.dto.base import ApplicationDTO

class UserDTO(ApplicationDTO):
    user_id: int
    surname: str
    name: str
    patronymic: Optional[str]
    phone_number: Optional[str]
    role: RoleEnum
    status: UserStatusEnum
    photos: List[str]
    telegram_id: Optional[int] = None
    chat_id: Optional[int] = None

    @classmethod
    def from_user(cls, user: User) -> 'UserDTO':
        return cls.from_model(user)
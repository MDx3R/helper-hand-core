from typing import Optional, List
from pydantic import BaseModel

from domain.models import User 
from domain.models.enums import RoleEnum, UserStatusEnum

class UserOutputDTO(BaseModel):
    """
    DTO выходных данных пользователя.

    Этот класс используется для представления данных пользователя на уровень представления.
    """

    user_id: int
    surname: str
    name: str
    patronymic: Optional[str]
    phone_number: Optional[str]
    role: RoleEnum 
    status: UserStatusEnum
    photos: List[str]
    telegram_id: int 
    chat_id: int

    @classmethod
    def from_user(cls, user: User) -> 'UserOutputDTO':
        """
        Преобразует `User` в `OrderOutputDTO`.
        """
        return cls(
            user_id=user.user_id,
            surname=user.surname,
            name=user.name,
            patronymic=user.patronymic,
            phone_number=user.phone_number,
            role=user.role,
            status=user.status,
            photos=user.photos,
            telegram_id=user.telegram_id,
            chat_id=user.chat_id
        )
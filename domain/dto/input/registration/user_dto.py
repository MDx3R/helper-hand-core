from typing import Optional, List
from datetime import date

from pydantic import Field

from domain.entities import User, Contractee, Contractor
from domain.entities.enums import RoleEnum, GenderEnum, CitizenshipEnum, PositionEnum
from domain.entities.base import ApplicationModel

class UserRegistrationDTO(ApplicationModel):
    surname: str
    name: str
    patronymic: Optional[str] = None
    phone_number: str
    role: RoleEnum 
    photos: List[str]

    def to_user(self) -> User:
        """
        Поле `status` устанавливается значением по умолчанию.
        """
        return User.model_validate(self.model_dump())

class UserResetDTO(UserRegistrationDTO):
    user_id: int

class WebUserRegistrationDTO(UserRegistrationDTO):
    pass

class TelegramUserRegistrationDTO(UserRegistrationDTO):
    telegram_id: int
    chat_id: int
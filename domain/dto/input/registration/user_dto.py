from typing import Optional, List
from datetime import date

from pydantic import Field

from domain.entities import User, Contractee, Contractor
from domain.entities.enums import RoleEnum, GenderEnum, CitizenshipEnum, PositionEnum
from domain.dto.base import ApplicationDTO

class UserRegistrationDTO(ApplicationDTO):
    user_id: None = None
    surname: str
    name: str
    patronymic: Optional[str] = None
    phone_number: str
    role: RoleEnum 
    photos: List[str]
    telegram_id: Optional[int] = None
    chat_id: Optional[int] = None

    def to_user(self) -> User:
        """
        Поле `status` устанавливается значением по умолчанию.
        """
        return User.model_validate(self.model_dump())

class UserResetDTO(UserRegistrationDTO):
    user_id: int
    telegram_id: int
    chat_id: int

class WebUserRegistrationDTO(UserRegistrationDTO):
    telegram_id: None = None
    chat_id: None = None

class TelegramUserRegistrationDTO(UserRegistrationDTO):
    telegram_id: int
    chat_id: int
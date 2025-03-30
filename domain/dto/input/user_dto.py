from typing import Optional, List

from domain.entities import User 
from domain.entities.enums import RoleEnum
from domain.entities.base import ApplicationModel

class UserInputDTO(ApplicationModel):
    user_id: Optional[int] = None
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
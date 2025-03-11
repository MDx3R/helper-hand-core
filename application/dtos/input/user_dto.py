from typing import Optional, List
from pydantic import BaseModel

from domain.models import User 
from domain.models.enums import RoleEnum

class UserInputDTO(BaseModel):
    """
    DTO входных данных пользователя.

    Этот класс используется для представления данных пользователя, полученных из внешнего источника. 
    Он предназначен для валидации входных данных перед передачей в бизнес-логику.
    """

    surname: str
    name: str
    patronymic: Optional[str] = None
    phone_number: str
    role: RoleEnum 
    photos: List[str]
    telegram_id: int 
    chat_id: int

    def to_user(self) -> User:
        """
        Преобразует `UserInputDTO` в `User`.
        
        Поле `status` устанавливается значением по умолчанию.
        """
        return User(
            surname=self.surname,
            name=self.name,
            patronymic=self.patronymic,
            phone_number=self.phone_number,
            role=self.role,
            photos=self.photos,
            telegram_id=self.telegram_id,
            chat_id=self.chat_id
        )
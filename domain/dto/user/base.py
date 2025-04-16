from typing import List, Optional

from domain.dto.base import ApplicationDTO


class UserBaseDTO(ApplicationDTO):
    surname: str
    name: str
    patronymic: Optional[str]


class TelegramCredentialsDTO(ApplicationDTO):
    telegram_id: int
    chat_id: int


class UserInputDTO(UserBaseDTO):
    phone_number: str
    photos: List[str]

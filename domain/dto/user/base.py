from typing import List, Optional

from domain.dto.base import ApplicationDTO


class UserBaseDTO(ApplicationDTO):
    surname: str
    name: str
    patronymic: Optional[str] = None


class TelegramCredentialsDTO(ApplicationDTO):
    telegram_id: int
    chat_id: int


class WebCredentialsDTO(ApplicationDTO):
    email: str


class UserCredentialsDTO(ApplicationDTO):
    telegram: Optional[TelegramCredentialsDTO] = None
    web: Optional[WebCredentialsDTO] = None


class WithCredentialsDTO(ApplicationDTO):
    credentials: UserCredentialsDTO

from typing import List, Optional

from domain.dto.base import ApplicationDTO
from domain.dto.user.base import (
    TelegramCredentialsDTO,
    UserBaseDTO,
    WebCredentialsDTO,
)


class UserInputDTO(UserBaseDTO):
    phone_number: str
    photos: List[str]


class TelegramCredentialsInputDTO(TelegramCredentialsDTO):
    pass


class WebCredentialsInputDTO(WebCredentialsDTO):
    password: str


class WithWebCredentialsInputDTO(ApplicationDTO):
    web: WebCredentialsInputDTO


class WithTelegramCredentialsInputDTO(ApplicationDTO):
    telegram: TelegramCredentialsInputDTO


class CredentialsInputDTO(ApplicationDTO):
    web: Optional[WebCredentialsInputDTO] = None
    telegram: Optional[TelegramCredentialsInputDTO] = None


class WithCredentialsInputDTO(ApplicationDTO):
    credentials: CredentialsInputDTO


class BaseRegisterUserDTO(WithCredentialsInputDTO):
    pass

import re
from typing import List, Optional

from pydantic import Field, field_validator

from domain.dto.base import ApplicationDTO
from domain.dto.user.base import (
    TelegramCredentialsDTO,
    WebCredentialsDTO,
)


class UserInputDTO(ApplicationDTO):
    surname: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=100)
    patronymic: Optional[str] = Field(None, min_length=1, max_length=100)
    phone_number: str
    photos: List[str]

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v: str) -> str:
        pattern = re.compile(r"^(?:\+7|8)\d{10}$")
        if not pattern.match(v):
            raise ValueError(
                "Invalid phone number format. Use +7XXXXXXXXXX or 89XXXXXXXXXX"
            )
        return v

    @field_validator("surname", "name", "patronymic")
    @classmethod
    def must_be_alphabetic(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.isalpha():
            raise ValueError("Поле должно содержать только буквы")
        return value


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

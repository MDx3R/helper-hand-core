from typing import List, Optional

from domain.dto.base import ApplicationDTO
from domain.dto.user.base import (
    TelegramCredentialsDTO,
    UserBaseDTO,
    WebCredentialsDTO,
)
from domain.entities.user.enums import RoleEnum, UserStatusEnum


class UserProfileOutputDTO(UserBaseDTO):
    user_id: int
    photos: List[str]
    role: RoleEnum
    status: UserStatusEnum


class UserOutputDTO(UserProfileOutputDTO):
    phone_number: str


class TelegramCredentialsOutputDTO(TelegramCredentialsDTO):
    user_id: int


class WebCredentialsOutputDTO(WebCredentialsDTO):
    user_id: int


class UserCredentialsOutputDTO(ApplicationDTO):
    telegram: Optional[TelegramCredentialsOutputDTO] = None
    web: Optional[WebCredentialsOutputDTO] = None


class WithCredentialsOutputDTO(ApplicationDTO):
    credentials: UserCredentialsOutputDTO


class CompleteUserOutputDTO(WithCredentialsOutputDTO):
    user: UserOutputDTO


class AuthOutputDTO(ApplicationDTO):
    access_token: str
    refresh_token: str


class WithAuthOutputDTO(ApplicationDTO):
    token: AuthOutputDTO

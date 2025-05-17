from typing import Generic, List, Optional, TypeVar

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


USER = TypeVar("USER", bound=UserOutputDTO)


class BaseCompleteUserOutputDTO(WithCredentialsOutputDTO):
    pass


class CompleteUserOutputDTO(BaseCompleteUserOutputDTO):
    user: UserOutputDTO


class AuthOutputDTO(ApplicationDTO):
    user_id: int
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class WithAuthOutputDTO(ApplicationDTO):
    token: AuthOutputDTO


class BaseUserRegistationOutputDTO(WithAuthOutputDTO):
    pass

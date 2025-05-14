from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field, fields
from datetime import date
from typing import Any, Generic, List, Optional, Self, Type, TypeVar

from domain.entities.enums import CitizenshipEnum, GenderEnum, PositionEnum
from domain.entities.user.admin.admin import Admin
from domain.entities.user.contractee.contractee import Contractee
from domain.entities.user.contractor.contractor import Contractor
from domain.entities.user.credentials import (
    TelegramCredentials,
    WebCredentials,
)
from domain.entities.user.enums import RoleEnum, UserStatusEnum
from domain.entities.user.user import User
from tests.data_generators import (
    AdminData,
    ContracteeData,
    ContractorData,
    TelegramCredentialsData,
    UserData,
    WebCredentialsData,
)


T = TypeVar("T")


class BaseBuilder(ABC, Generic[T]):
    @abstractmethod
    def build(self) -> T:
        pass


class BaseUserBuilder(BaseBuilder[T]):
    def __init__(self, data: UserData):
        self._user = data

    def with_user_id(self, user_id: int) -> Self:
        self._user.user_id = user_id
        return self

    def with_surname(self, surname: str) -> Self:
        self._user.surname = surname
        return self

    def with_name(self, name: str) -> Self:
        self._user.name = name
        return self

    def with_patronymic(self, patronymic: str | None) -> Self:
        self._user.patronymic = patronymic
        return self

    def with_phone_number(self, phone_number: str) -> Self:
        self._user.phone_number = phone_number
        return self

    def with_role(self, role: RoleEnum) -> Self:
        self._user.role = role
        return self

    def with_status(self, status: UserStatusEnum) -> Self:
        self._user.status = status
        return self

    def with_photos(self, photos: List[str]) -> Self:
        self._user.photos = photos
        return self


class BaseContractorBuilder(BaseUserBuilder[T]):
    def __init__(self, data: ContractorData):
        self._user = data

    def with_about(self, about: str) -> Self:
        self._user.about = about
        return self


class BaseContracteeBuilder(BaseUserBuilder[T]):
    def __init__(self, data: ContracteeData):
        self._user = data

    def with_birthday(self, birthday: date) -> Self:
        self._user.birthday = birthday
        return self

    def with_height(self, height: int) -> Self:
        self._user.height = height
        return self

    def with_gender(self, gender: GenderEnum) -> Self:
        self._user.gender = gender
        return self

    def with_citizenship(self, citizenship: CitizenshipEnum) -> Self:
        self._user.citizenship = citizenship
        return self

    def with_positions(self, positions: List[PositionEnum]) -> Self:
        self._user.positions = positions
        return self


class BaseAdminBuilder(BaseUserBuilder[T]):
    def __init__(self, data: AdminData):
        self._user = data

    def with_about(self, about: str) -> Self:
        self._user.about = about
        return self

    def with_contractor_id(self, contractor_id: int) -> Self:
        self._user.contractor_id = contractor_id
        return self


class UserBuilder(BaseUserBuilder):
    def build(self) -> User:
        return User(**asdict(self._user))


class ContractorBuilder(BaseContractorBuilder):
    def build(self) -> Contractor:
        return Contractor(
            **asdict(self._user) | {"contractor_id": self._user.user_id}
        )


class ContracteeBuilder(BaseContracteeBuilder):
    def build(self) -> Contractee:
        return Contractee(
            **asdict(self._user) | {"contractee_id": self._user.user_id}
        )


class AdminBuilder(BaseAdminBuilder):
    def build(self) -> Admin:
        return Admin(**asdict(self._user) | {"admin_id": self._user.user_id})


class BaseTelegramCredentialsBuilder(BaseBuilder):
    def __init__(self, data: TelegramCredentialsData):
        self._creds = data

    def with_user_id(self, user_id: int) -> Self:
        self._creds.user_id = user_id
        return self

    def with_telegram_id(self, telegram_id: int) -> Self:
        self._creds.telegram_id = telegram_id
        return self

    def with_chat_id(self, chat_id: int) -> Self:
        self._creds.chat_id = chat_id
        return self


class BaseWebCredentialsBuilder(BaseBuilder):
    def __init__(self, data: WebCredentialsData):
        self._creds = data

    def with_user_id(self, user_id: int) -> Self:
        self._creds.user_id = user_id
        return self

    def with_email(self, email: str) -> Self:
        self._creds.email = email
        return self

    def with_password(self, password: str) -> Self:
        self._creds.password = password
        return self


class TelegramCredentialsBuilder(BaseTelegramCredentialsBuilder):
    def build(self) -> TelegramCredentials:
        return TelegramCredentials(**asdict(self._creds))


class WebCredentialsBuilder(BaseWebCredentialsBuilder):
    def build(self) -> WebCredentials:
        return WebCredentials(**asdict(self._creds))

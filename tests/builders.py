from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field, fields
from datetime import date
from typing import Any, Generic, List, Optional, Self, Type, TypeVar

from domain.dto.user.response.admin.admin_output_dto import (
    AdminOutputDTO,
)
from domain.dto.user.response.contractee.contractee_output_dto import (
    ContracteeOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    ContractorOutputDTO,
)
from domain.dto.user.response.user_output_dto import (
    TelegramCredentialsOutputDTO,
    UserOutputDTO,
    WebCredentialsOutputDTO,
)
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


@dataclass
class UserData:
    user_id: Optional[int] = 1
    surname: str = "Doe"
    name: str = "John"
    patronymic: Optional[str] = None
    phone_number: str = "1234567890"
    role: RoleEnum = RoleEnum.contractor
    status: UserStatusEnum = UserStatusEnum.created
    photos: List[str] = field(default_factory=list)


@dataclass
class ContractorData(UserData):
    about: str = ""


@dataclass
class ContracteeData(UserData):
    birthday: date = date(2000, 1, 1)
    height: int = 180
    gender: GenderEnum.male = GenderEnum.male
    citizenship: CitizenshipEnum = CitizenshipEnum.russia
    positions: List[PositionEnum] = field(default_factory=list)


@dataclass
class AdminData(UserData):
    about: str = ""
    contractor_id: Optional[str] = None


@dataclass
class TelegramCredentialsData:
    user_id: int
    telegram_id: int = 123456789
    chat_id: int = 123456789


@dataclass
class WebCredentialsData:
    user_id: int
    email: str = "mail@site.com"
    password: str = "password"


T = TypeVar("T")
C = TypeVar("C", bound=UserData)


def filter_fields_by_class(cls: Type, data: dict[str, Any]) -> dict[str, Any]:
    allowed_keys = {f.name for f in fields(cls)}
    return {k: data[k] for k in data if k in allowed_keys}


def dataclass_builder(cls: type[T], data: dict[str, Any]) -> T:
    return cls(**filter_fields_by_class(cls, data))


class BaseBuilder(ABC, Generic[T]):
    def __init__(self, data: dict[str, Any] = None):
        self._data = data or {}
        self._init_builder(self._data)

    @abstractmethod
    def _init_builder(self, data: dict[str, Any]):
        pass

    @abstractmethod
    def build(self) -> T:
        pass


class ModelBuilder(BaseBuilder[T]):
    def __init__(self, cls: type[T], data: dict[str, Any]):
        self._cls = cls
        self._data = data

    def _init_builder(self, data: dict[str, Any]):
        pass

    def build(self) -> T:
        return self._cls(**self._data)


class BaseUserBuilder(BaseBuilder[T]):
    def _init_builder(self, data: dict[str, Any]):
        self._user = dataclass_builder(UserData, data)

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
    def _init_builder(self, data: dict[str, Any]):
        self._user = dataclass_builder(ContractorData, data)

    def with_about(self, about: str) -> Self:
        self._user.about = about
        return self


class BaseContracteeBuilder(BaseUserBuilder[T]):
    def _init_builder(self, data: dict[str, Any]):
        self._user = dataclass_builder(ContracteeData, data or {})

    def with_birthday(self, birthday: date) -> Self:
        self._birthday = birthday
        return self

    def with_height(self, height: int) -> Self:
        self._height = height
        return self

    def with_gender(self, gender: GenderEnum) -> Self:
        self._gender = gender
        return self

    def with_citizenship(self, citizenship: CitizenshipEnum) -> Self:
        self._citizenship = citizenship
        return self

    def with_positions(self, positions: List[PositionEnum]) -> Self:
        self._positions = positions
        return self


class BaseAdminBuilder(BaseUserBuilder[T]):
    def _init_builder(self, data: dict[str, Any]):
        self._user = dataclass_builder(AdminData, data)

    def with_about(self, about: str) -> Self:
        self._about = about
        return self

    def with_contractor_id(self, contractor_id: int) -> Self:
        self._contractor_id = contractor_id
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
    def _init_builder(self, data: dict[str, Any]):
        self._creds = dataclass_builder(TelegramCredentialsData, data)

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
    def _init_builder(self, data: dict[str, Any]):
        self._creds = dataclass_builder(WebCredentialsData, data)

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

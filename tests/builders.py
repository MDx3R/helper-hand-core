from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field, fields
from datetime import date, datetime
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
from domain.entities.order.order import Order
from domain.entities.order.detail import OrderDetail
from domain.entities.reply.reply import Reply
from tests.data_generators import (
    AdminData,
    ContracteeData,
    ContractorData,
    TelegramCredentialsData,
    UserData,
    WebCredentialsData,
    OrderData,
    OrderDetailData,
    ReplyData,
)
from domain.entities.order.enums import OrderStatusEnum
from domain.entities.reply.enums import ReplyStatusEnum


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


class BaseOrderBuilder(BaseBuilder[T]):
    def __init__(self, data: OrderData):
        self._order = data

    def with_order_id(self, order_id: int) -> Self:
        self._order.order_id = order_id
        return self

    def with_contractor_id(self, contractor_id: int) -> Self:
        self._order.contractor_id = contractor_id
        return self

    def with_about(self, about: str) -> Self:
        self._order.about = about
        return self

    def with_address(self, address: str) -> Self:
        self._order.address = address
        return self

    def with_admin_id(self, admin_id: int | None) -> Self:
        self._order.admin_id = admin_id
        return self

    def with_status(self, status: OrderStatusEnum) -> Self:
        self._order.status = status
        return self

    def with_created_at(self, created_at: datetime) -> Self:
        self._order.created_at = created_at
        return self

    def with_updated_at(self, updated_at: datetime) -> Self:
        self._order.updated_at = updated_at
        return self


class OrderBuilder(BaseOrderBuilder):
    def build(self) -> Order:
        return Order(**asdict(self._order))


class BaseOrderDetailBuilder(BaseBuilder[T]):
    def __init__(self, data: OrderDetailData):
        self._detail = data

    def with_detail_id(self, detail_id: int) -> Self:
        self._detail.detail_id = detail_id
        return self

    def with_order_id(self, order_id: int) -> Self:
        self._detail.order_id = order_id
        return self

    def with_date(self, date_: date) -> Self:
        self._detail.date = date_
        return self

    def with_start_at(self, start_at: Any) -> Self:
        self._detail.start_at = start_at
        return self

    def with_end_at(self, end_at: Any) -> Self:
        self._detail.end_at = end_at
        return self

    def with_position(self, position: PositionEnum) -> Self:
        self._detail.position = position
        return self

    def with_count(self, count: int) -> Self:
        self._detail.count = count
        return self

    def with_wager(self, wager: int) -> Self:
        self._detail.wager = wager
        return self

    def with_fee(self, fee: int) -> Self:
        self._detail.fee = fee
        return self

    def with_gender(self, gender: GenderEnum | None) -> Self:
        self._detail.gender = gender
        return self

    def with_created_at(self, created_at: datetime) -> Self:
        self._detail.created_at = created_at
        return self

    def with_updated_at(self, updated_at: datetime) -> Self:
        self._detail.updated_at = updated_at
        return self


class OrderDetailBuilder(BaseOrderDetailBuilder):
    def build(self) -> OrderDetail:
        return OrderDetail(**asdict(self._detail))


class BaseReplyBuilder(BaseBuilder[T]):
    def __init__(self, data: ReplyData):
        self._reply = data

    def with_contractee_id(self, contractee_id: int) -> Self:
        self._reply.contractee_id = contractee_id
        return self

    def with_detail_id(self, detail_id: int) -> Self:
        self._reply.detail_id = detail_id
        return self

    def with_wager(self, wager: int) -> Self:
        self._reply.wager = wager
        return self

    def with_status(self, status: ReplyStatusEnum) -> Self:
        self._reply.status = status
        return self

    def with_paid(self, paid: datetime | None) -> Self:
        self._reply.paid = paid
        return self

    def with_created_at(self, created_at: datetime) -> Self:
        self._reply.created_at = created_at
        return self

    def with_updated_at(self, updated_at: datetime) -> Self:
        self._reply.updated_at = updated_at
        return self


class ReplyBuilder(BaseReplyBuilder):
    def build(self) -> Reply:
        return Reply(**asdict(self._reply))

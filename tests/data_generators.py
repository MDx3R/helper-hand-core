from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field, fields
from datetime import date, datetime
from typing import Any, List, Optional, Type, TypeVar
from enum import Enum
from typing import Any, Optional
from faker import Faker

from domain.entities.enums import CitizenshipEnum, GenderEnum, PositionEnum
from domain.entities.order.enums import OrderStatusEnum
from domain.entities.reply.enums import ReplyStatusEnum
from domain.entities.user.enums import RoleEnum, UserStatusEnum
from domain.wager import calculate_pay

fake = Faker("ru_RU")


T = TypeVar("T")


def filter_fields_by_class(cls: Type, data: dict[str, Any]) -> dict[str, Any]:
    allowed_keys = {f.name for f in fields(cls)}
    return {k: data[k] for k in data if k in allowed_keys}


def dataclass_builder(cls: type[T], data: dict[str, Any]) -> T:
    return cls(**filter_fields_by_class(cls, data))


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
    gender: GenderEnum = GenderEnum.male
    citizenship: CitizenshipEnum = CitizenshipEnum.russia
    positions: List[PositionEnum] = field(default_factory=list)


@dataclass
class AdminData(UserData):
    about: str = ""
    contractor_id: Optional[int] = None


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


@dataclass
class OrderData:
    order_id: int
    contractor_id: int
    about: str
    address: str
    admin_id: Optional[int]
    status: OrderStatusEnum
    created_at: datetime
    updated_at: datetime


@dataclass
class OrderDetailData:
    detail_id: int
    order_id: int
    date: date
    start_at: Any
    end_at: Any
    position: PositionEnum
    count: int
    wager: int
    fee: int
    gender: Optional[GenderEnum]
    created_at: datetime
    updated_at: datetime


@dataclass
class ReplyData:
    contractee_id: int
    detail_id: int
    wager: int
    status: ReplyStatusEnum
    paid: Optional[datetime]
    created_at: datetime
    updated_at: datetime


ENUM = TypeVar("ENUM", bound=Enum)


class DataGenerator(ABC):
    @staticmethod
    def get_id() -> int:
        return fake.unique.random_int(min=1, max=100)

    @staticmethod
    def get_telegram_id() -> int:
        return fake.unique.random_int(min=100000, max=999999999)

    @staticmethod
    def get_created_at() -> datetime:
        return fake.date_time_this_year()

    @staticmethod
    def get_updated_at() -> datetime:
        return fake.date_time_this_year()

    @staticmethod
    def get_optional_id() -> Optional[int]:
        return fake.random_element(
            elements=[None, fake.random_int(min=1, max=100)]
        )

    @staticmethod
    def get_enum_value(enum_cls: type[Enum]) -> Enum:
        return fake.random_element(elements=[e for e in enum_cls])

    @staticmethod
    def get_image_urls(count: int = 2) -> list[str]:
        return [fake.image_url() for _ in range(count)]

    @abstractmethod
    def generate(self):
        pass


class UserDataGenerator(DataGenerator):
    def generate(self) -> UserData:
        return UserData(
            user_id=self.get_id(),
            surname=fake.last_name(),
            name=fake.first_name(),
            patronymic=fake.middle_name(),
            phone_number=fake.unique.phone_number(),
            role=self.get_enum_value(RoleEnum),
            status=self.get_enum_value(UserStatusEnum),
            photos=self.get_image_urls(),
        )


class ContractorDataGenerator(UserDataGenerator):
    def generate(self) -> ContractorData:
        base = super().generate()
        return ContractorData(**base.__dict__, about=fake.paragraph())


class ContracteeDataGenerator(UserDataGenerator):
    def generate(self) -> ContracteeData:
        base = super().generate()
        return ContracteeData(
            **base.__dict__,
            birthday=fake.date_of_birth(minimum_age=18, maximum_age=60),
            height=fake.random_int(min=150, max=200),
            gender=self.get_enum_value(GenderEnum),
            citizenship=self.get_enum_value(CitizenshipEnum),
            positions=fake.random_elements(
                elements=[e for e in PositionEnum],
                length=fake.random_int(min=1, max=3),
            ),
        )


class AdminDataGenerator(UserDataGenerator):
    def generate(self) -> AdminData:
        base = super().generate()
        return AdminData(
            **base.__dict__,
            about=fake.paragraph(),
            contractor_id=fake.random_element(elements=[None, base.user_id]),
        )


class TelegramCredentialsDataGenerator(DataGenerator):
    def generate(self) -> TelegramCredentialsData:
        return TelegramCredentialsData(
            user_id=self.get_id(),
            telegram_id=self.get_telegram_id(),
            chat_id=self.get_telegram_id(),
        )


class WebCredentialsDataGenerator(DataGenerator):
    def generate(self) -> WebCredentialsData:
        return WebCredentialsData(
            user_id=self.get_id(),
            email=fake.email(),
            password=fake.password(),
        )


class OrderDataGenerator(DataGenerator):
    @staticmethod
    def _generate() -> OrderData:
        return OrderData(
            order_id=DataGenerator.get_id(),
            contractor_id=DataGenerator.get_id(),
            about=fake.sentence(),
            address=fake.address(),
            admin_id=DataGenerator.get_optional_id(),
            status=DataGenerator.get_enum_value(OrderStatusEnum),
            created_at=DataGenerator.get_created_at(),
            updated_at=DataGenerator.get_updated_at(),
        )


class OrderDetailDataGenerator(DataGenerator):
    @staticmethod
    def _generate() -> OrderDetailData:
        wager = fake.random_int(min=100, max=1000)
        return OrderDetailData(
            detail_id=DataGenerator.get_id(),
            order_id=DataGenerator.get_id(),
            date=fake.date_this_year(),
            start_at=fake.time_object(),
            end_at=fake.time_object(),
            position=DataGenerator.get_enum_value(PositionEnum),
            count=fake.random_int(min=1, max=10),
            wager=wager,
            fee=wager - calculate_pay(wager),
            gender=fake.random_element(elements=[*GenderEnum, None]),
            created_at=DataGenerator.get_created_at(),
            updated_at=DataGenerator.get_updated_at(),
        )


class ReplyDataGenerator(DataGenerator):
    @staticmethod
    def _generate() -> ReplyData:
        return ReplyData(
            contractee_id=DataGenerator.get_id(),
            detail_id=DataGenerator.get_id(),
            wager=fake.random_int(min=100, max=1000),
            status=DataGenerator.get_enum_value(ReplyStatusEnum),
            paid=fake.random_element(
                elements=[None, DataGenerator.get_created_at()]
            ),
            created_at=DataGenerator.get_created_at(),
            updated_at=DataGenerator.get_updated_at(),
        )

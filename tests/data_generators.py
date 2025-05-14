from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
import random
from typing import Any, Optional
from faker import Faker

from domain.entities.enums import CitizenshipEnum, GenderEnum, PositionEnum
from domain.entities.order.enums import OrderStatusEnum
from domain.entities.reply.enums import ReplyStatusEnum
from domain.entities.user.enums import RoleEnum, UserStatusEnum
from domain.wager import calculate_pay


fake = Faker("ru_RU")


class DataGenerator(ABC):
    def __init__(self):
        self._data = None

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

    def generate(cls) -> dict[str, Any]:
        cls._data = cls._data or cls._generate()
        return cls._data

    @staticmethod
    @abstractmethod
    def _generate(cls) -> dict[str, Any]:
        pass


class UserDataGenerator(DataGenerator):
    @staticmethod
    def _generate() -> dict[str, Any]:
        return {
            "user_id": DataGenerator.get_id(),
            "surname": fake.last_name(),
            "name": fake.first_name(),
            "patronymic": fake.middle_name(),
            "phone_number": fake.unique.phone_number(),
            "role": DataGenerator.get_enum_value(RoleEnum),
            "telegram_id": DataGenerator.get_telegram_id(),
            "chat_id": DataGenerator.get_telegram_id(),
            "status": DataGenerator.get_enum_value(UserStatusEnum),
            "photos": DataGenerator.get_image_urls(),
            "created_at": DataGenerator.get_created_at(),
            "updated_at": DataGenerator.get_updated_at(),
        }


class OrderDataGenerator(DataGenerator):
    @staticmethod
    def _generate() -> dict[str, Any]:
        return {
            "order_id": DataGenerator.get_id(),
            "contractor_id": DataGenerator.get_id(),
            "about": fake.sentence(),
            "address": fake.address(),
            "admin_id": DataGenerator.get_optional_id(),
            "status": DataGenerator.get_enum_value(OrderStatusEnum),
            "created_at": DataGenerator.get_created_at(),
            "updated_at": DataGenerator.get_updated_at(),
        }


class OrderDetailDataGenerator(DataGenerator):
    @staticmethod
    def _generate() -> dict[str, Any]:
        wager = fake.random_int(min=100, max=1000)
        return {
            "detail_id": DataGenerator.get_id(),
            "order_id": DataGenerator.get_id(),
            "date": fake.date_this_year(),
            "start_at": fake.time_object(),
            "end_at": fake.time_object(),
            "position": DataGenerator.get_enum_value(PositionEnum),
            "count": fake.random_int(min=1, max=10),
            "wager": wager,
            "fee": wager - calculate_pay(wager),
            "gender": fake.random_element(elements=[*GenderEnum, None]),
            "created_at": DataGenerator.get_created_at(),
            "updated_at": DataGenerator.get_updated_at(),
        }


class ReplyDataGenerator(DataGenerator):
    @staticmethod
    def _generate() -> dict[str, Any]:
        return {
            "contractee_id": DataGenerator.get_id(),
            "detail_id": DataGenerator.get_id(),
            "wager": fake.random_int(min=100, max=1000),
            "status": DataGenerator.get_enum_value(ReplyStatusEnum),
            "paid": fake.random_element(
                elements=[None, DataGenerator.get_created_at()]
            ),
            "created_at": DataGenerator.get_created_at(),
            "updated_at": DataGenerator.get_updated_at(),
        }


class AdminDataGenerator(UserDataGenerator):
    @staticmethod
    def _generate() -> dict[str, Any]:
        user_data = super().generate()

        return user_data | {
            "admin_id": user_data["user_id"],
            "role": RoleEnum.admin,
            "about": fake.paragraph(),
            "contractor_id": fake.random_element(
                elements=[None, user_data["user_id"]]
            ),
        }


class ContractorDataGenerator(UserDataGenerator):
    @staticmethod
    def _generate() -> dict[str, Any]:
        user_data = super().generate()
        return user_data | {
            "contractor_id": user_data["user_id"],
            "role": RoleEnum.contractor,
            "about": fake.paragraph(),
        }


class ContracteeDataGenerator(UserDataGenerator):
    @staticmethod
    def _generate() -> dict[str, Any]:
        user_data = super().generate()
        return user_data | {
            "contractee_id": user_data["user_id"],
            "role": RoleEnum.contractee,
            "birthday": fake.date_of_birth(minimum_age=18, maximum_age=60),
            "height": fake.random_int(min=150, max=200),
            "gender": DataGenerator.get_enum_value(GenderEnum),
            "citizenship": DataGenerator.get_enum_value(CitizenshipEnum),
            "positions": fake.random_elements(
                elements=[e for e in PositionEnum],
                length=fake.random_int(min=1, max=3),
            ),
        }

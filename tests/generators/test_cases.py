from dataclasses import dataclass
from typing import List, TypeVar

from domain.dto.common import UserDTO
from domain.dto.common.detailed_order_dto import DetailedOrderDTO
from domain.dto.context import UserContextDTO
from domain.dto.input.order_detail_dto import OrderDetailInputDTO
from domain.dto.input.order_dto import OrderInputDTO
from domain.dto.input.registration import UserRegistrationDTO, UserResetDTO
from domain.dto.internal import ResetDTO
from domain.entities import ApplicationModel
from infrastructure.database.mappers import Mapper
from infrastructure.database.models import Base, UserBase
from tests.generators.base import B, M

MAP = TypeVar("M", bound=Mapper)


class TestCase:
    pass


@dataclass
class ApplicationModelTestCase(TestCase):
    model: ApplicationModel


@dataclass
class BaseTestCase(TestCase):
    base: Base


@dataclass
class UserRegistrationTestCase(TestCase):
    input: UserRegistrationDTO
    expected: UserDTO


@dataclass
class UserResetTestCase(TestCase):
    reset: ResetDTO
    expected: UserDTO


@dataclass
class CreateOrderTestCase(TestCase):
    order: OrderInputDTO
    details: List[OrderDetailInputDTO]
    expected: DetailedOrderDTO


@dataclass
class MapperTestCase:
    mapper: MAP
    base: B
    model: M


@dataclass
class AggregatedUserMapperTestCase:
    mapper: MAP
    user_base: UserBase
    role_base: B
    model: M

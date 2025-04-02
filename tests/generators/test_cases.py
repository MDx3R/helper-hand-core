from typing import TypeVar
from dataclasses import dataclass

from domain.entities import ApplicationModel
from domain.dto.input.registration import UserRegistrationDTO, UserResetDTO
from domain.dto.internal import ResetDTO
from domain.dto.context import UserContextDTO
from domain.dto.common import UserDTO

from infrastructure.database.models import Base, UserBase
from infrastructure.database.mappers import Mapper

from tests.generators.base import (
    B, M
)

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
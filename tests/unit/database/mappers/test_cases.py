from typing import TypeVar
from dataclasses import dataclass

from infrastructure.database.mappers import Mapper
from infrastructure.database.models import UserBase
from tests.generators.base import (
    B, M
)

MAP = TypeVar("M", bound=Mapper)

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
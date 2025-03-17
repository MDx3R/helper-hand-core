from typing import Generic, TypeVar, List
from dataclasses import dataclass
from datetime import datetime

from domain.models import ApplicationModel, User, Order, OrderDetail, Reply, Contractee, Contractor, Admin
from infrastructure.database.models import Base, UserBase, OrderBase, OrderDetailBase, ReplyBase, ContracteeBase, ContractorBase, AdminBase
from infrastructure.database.mappers import (
    Mapper, ApplicationModelMapper, UserMapper, OrderMapper, OrderDetailMapper, ReplyMapper,
    AggregatedUserMapper, ContracteeMapper, ContractorMapper, AdminMapper
)
from tests.creators import (
    ModelBaseCreator, UserCreator, OrderCreator, OrderDetailCreator, ReplyCreator,
    AggregatedUserCreator, ContracteeCreator, ContractorCreator, AdminCreator
)
from tests.generators.base import ApplicationModelTestCasesGenerator, BaseTestCasesGenerator
from .test_cases import MAP, B, M, MapperTestCase, AggregatedUserMapperTestCase

MAP = TypeVar("MAP", bound=Mapper)

class MapperTestCasesGenerator(
    ApplicationModelTestCasesGenerator[MapperTestCase, M],
    BaseTestCasesGenerator[MapperTestCase, B],
    Generic[MAP, B, M]
):
    mapper: type[Mapper] = Mapper
    creator: type[ModelBaseCreator] = ModelBaseCreator

    @classmethod
    def _create_test_case(cls, **kwargs) -> MapperTestCase:
        base, model = cls.creator.get_default_pair(**kwargs)
        return MapperTestCase(cls._get_mapper(), base, model)

    @classmethod
    def _get_mapper(cls) -> MAP:
        return cls.mapper

class UserMapperTestCasesGenerator(MapperTestCasesGenerator[UserMapper, UserBase, User]):
    mapper = UserMapper
    creator = UserCreator
    presets = MapperTestCasesGenerator.presets | {
        "no_id": {"user_id": None},
        "no_patronymic": {"patronymic": None},
        "no_photos": {"photos": []},
    }

    @classmethod
    def create_no_id(cls):
        return cls.create("no_id")

    @classmethod
    def create_no_patronymic(cls):
        return cls.create("no_patronymic")

    @classmethod
    def create_no_photos(cls):
        return cls.create("no_photos")

class OrderMapperTestCasesGenerator(MapperTestCasesGenerator[OrderMapper, OrderBase, Order]):
    mapper = OrderMapper
    creator = OrderCreator
    presets = MapperTestCasesGenerator.presets | {
        "no_id": {"order_id": None},
        "no_admin_id": {"admin_id": None},
    }

    @classmethod
    def create_no_id(cls):
        return cls.create("no_id")

    @classmethod
    def create_no_admin_id(cls):
        return cls.create("no_admin_id")

class OrderDetailMapperTestCasesGenerator(MapperTestCasesGenerator[OrderDetailMapper, OrderDetailBase, OrderDetail]):
    mapper = OrderDetailMapper
    creator = OrderDetailCreator
    presets = MapperTestCasesGenerator.presets | {
        "no_id": {"detail_id": None},
        "no_gender": {"gender": None},
    }

    @classmethod
    def create_no_id(cls):
        return cls.create("no_id")

    @classmethod
    def create_no_gender(cls):
        return cls.create("no_gender")

class ReplyMapperTestCasesGenerator(MapperTestCasesGenerator[ReplyMapper, ReplyBase, Reply]):
    mapper = ReplyMapper
    creator = ReplyCreator
    presets = MapperTestCasesGenerator.presets | {
        "no_paid": {"paid": None},
    }

    @classmethod
    def create_no_paid(cls):
        return cls.create("no_paid")

class AggregatedUserMapperTestCasesGenerator(
    ApplicationModelTestCasesGenerator[AggregatedUserMapperTestCase, M],
    BaseTestCasesGenerator[AggregatedUserMapperTestCase, B],
    Generic[MAP, B, M]
):
    mapper: type[AggregatedUserMapper] = AggregatedUserMapper
    creator: type[AggregatedUserCreator] = AggregatedUserCreator

    @classmethod
    def _create_test_case(cls, **kwargs) -> AggregatedUserMapperTestCase:
        user_base = cls.creator.create_user_base()
        role_base, model = cls.creator.get_default_pair(**kwargs)
        return AggregatedUserMapperTestCase(cls._get_mapper(), user_base, role_base, model)

    @classmethod
    def _get_mapper(cls) -> MAP:
        return cls.mapper

    @classmethod
    def create_different_update_time(cls) -> AggregatedUserMapperTestCase:
        return cls._create_test_case(updated_at=datetime(2024, 3, 16, 13, 30, 0))

    @classmethod
    def _create_user_base(cls, data: dict) -> UserBase:
        return UserCreator.create_base(data)

class ContracteeMapperTestCasesGenerator(AggregatedUserMapperTestCasesGenerator[ContracteeMapper, ContracteeBase, Contractee]):
    mapper = ContracteeMapper
    creator = ContracteeCreator
    presets = AggregatedUserMapperTestCasesGenerator.presets | {
        "no_id": {"contractee_id": None},
    }

    @classmethod
    def create_no_id(cls):
        return cls.create("no_id")

class ContractorMapperTestCasesGenerator(AggregatedUserMapperTestCasesGenerator[ContractorMapper, ContractorBase, Contractor]):
    mapper = ContractorMapper
    creator = ContractorCreator
    presets = AggregatedUserMapperTestCasesGenerator.presets | {
        "no_id": {"contractor_id": None}, 
    }

    @classmethod
    def create_no_id(cls):
        return cls.create("no_id")

class AdminMapperTestCasesGenerator(AggregatedUserMapperTestCasesGenerator[AdminMapper, AdminBase, Admin]):
    mapper = AdminMapper
    creator = AdminCreator
    presets = AggregatedUserMapperTestCasesGenerator.presets | {
        "no_id": {"admin_id": None},
        "no_contractor_id": {"contractor_id": None},
    }

    @classmethod
    def create_no_id(cls):
        return cls.create("no_id")

    @classmethod
    def create_no_contractor_id(cls):
        return cls.create("no_contractor_id")
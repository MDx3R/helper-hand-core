from typing import Generic, TypeVar
from datetime import datetime

from domain.entities import (
    User, 
    Order, 
    OrderDetail, 
    Reply, 
    Contractee, 
    Contractor, 
    Admin
)
from infrastructure.database.models import (
    UserBase, 
    OrderBase, 
    OrderDetailBase, 
    ReplyBase, 
    ContracteeBase, 
    ContractorBase, 
    AdminBase
)
from infrastructure.database.mappers import (
    Mapper, UserMapper, OrderMapper, OrderDetailMapper, ReplyMapper,
    AggregatedUserMapper, ContracteeMapper, ContractorMapper, AdminMapper
)
from tests.factories import (
    ModelBaseFactory, UserFactory, OrderFactory, OrderDetailFactory, ReplyFactory,
    AggregatedUserFactory, ContracteeFactory, ContractorFactory, AdminFactory
)
from tests.generators.base import (
    ApplicationModelTestCaseGenerator, 
    BaseTestCaseGenerator, 
    GenerateAllTestCaseMixin
)
from .test_cases import MAP, B, M, MapperTestCase, AggregatedUserMapperTestCase

MAP = TypeVar("MAP", bound=Mapper)

class MapperTestCaseGenerator(
    ApplicationModelTestCaseGenerator[MapperTestCase, M],
    BaseTestCaseGenerator[MapperTestCase, B],
    GenerateAllTestCaseMixin,
    Generic[MAP, B, M]
):
    mapper: type[Mapper] = Mapper
    factory: type[ModelBaseFactory] = ModelBaseFactory

    @classmethod
    def _create_test_case(cls, **kwargs) -> MapperTestCase:
        base, model = cls.factory.get_random_pair(**kwargs)

        return MapperTestCase(cls._get_mapper(), base, model)

    @classmethod
    def _get_mapper(cls) -> MAP:
        return cls.mapper

class UserMapperTestCaseGenerator(
    MapperTestCaseGenerator[UserMapper, UserBase, User]
):
    mapper = UserMapper
    factory = UserFactory
    presets = MapperTestCaseGenerator.presets | {
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

class OrderMapperTestCaseGenerator(
    MapperTestCaseGenerator[OrderMapper, OrderBase, Order]
):
    mapper = OrderMapper
    factory = OrderFactory
    presets = MapperTestCaseGenerator.presets | {
        "no_id": {"order_id": None},
        "no_admin_id": {"admin_id": None},
    }

    @classmethod
    def create_no_id(cls):
        return cls.create("no_id")

    @classmethod
    def create_no_admin_id(cls):
        return cls.create("no_admin_id")

class OrderDetailMapperTestCaseGenerator(
    MapperTestCaseGenerator[OrderDetailMapper, OrderDetailBase, OrderDetail]
):
    mapper = OrderDetailMapper
    factory = OrderDetailFactory
    presets = MapperTestCaseGenerator.presets | {
        "no_id": {"detail_id": None},
        "no_gender": {"gender": None},
    }

    @classmethod
    def create_no_id(cls):
        return cls.create("no_id")

    @classmethod
    def create_no_gender(cls):
        return cls.create("no_gender")

class ReplyMapperTestCaseGenerator(
    MapperTestCaseGenerator[ReplyMapper, ReplyBase, Reply]
):
    mapper = ReplyMapper
    factory = ReplyFactory
    presets = MapperTestCaseGenerator.presets | {
        "no_paid": {"paid": None},
    }

    @classmethod
    def create_no_paid(cls):
        return cls.create("no_paid")

class AggregatedUserMapperTestCaseGenerator(
    ApplicationModelTestCaseGenerator[AggregatedUserMapperTestCase, M],
    BaseTestCaseGenerator[AggregatedUserMapperTestCase, B],
    GenerateAllTestCaseMixin,
    Generic[MAP, B, M]
):
    mapper: type[AggregatedUserMapper] = AggregatedUserMapper
    factory: type[AggregatedUserFactory] = AggregatedUserFactory

    @classmethod
    def _create_test_case(cls, **kwargs) -> AggregatedUserMapperTestCase:
        data = cls.factory.get_random_data()
        user_base = cls.factory.create_user_base(**data)
        role_base, model = cls.factory.get_default_pair(**(data | kwargs))

        return AggregatedUserMapperTestCase(cls._get_mapper(), user_base, role_base, model)

    @classmethod
    def _get_mapper(cls) -> MAP:
        return cls.mapper

    @classmethod
    def create_different_update_time(cls) -> AggregatedUserMapperTestCase:
        return cls._create_test_case(updated_at=datetime(2024, 3, 16, 13, 30, 0))

class ContracteeMapperTestCaseGenerator(
    AggregatedUserMapperTestCaseGenerator[
        ContracteeMapper, ContracteeBase, Contractee
    ]
):
    mapper = ContracteeMapper
    factory = ContracteeFactory
    presets = AggregatedUserMapperTestCaseGenerator.presets | {
        "no_id": {"contractee_id": None},
    }

    @classmethod
    def create_no_id(cls):
        return cls.create("no_id")

class ContractorMapperTestCaseGenerator(
    AggregatedUserMapperTestCaseGenerator[
        ContractorMapper, ContractorBase, Contractor
    ]
):
    mapper = ContractorMapper
    factory = ContractorFactory
    presets = AggregatedUserMapperTestCaseGenerator.presets | {
        "no_id": {"contractor_id": None}, 
    }

    @classmethod
    def create_no_id(cls):
        return cls.create("no_id")

class AdminMapperTestCaseGenerator(
    AggregatedUserMapperTestCaseGenerator[
        AdminMapper, AdminBase, Admin
    ]
):
    mapper = AdminMapper
    factory = AdminFactory
    presets = AggregatedUserMapperTestCaseGenerator.presets | {
        "no_id": {"admin_id": None},
        "no_contractor_id": {"contractor_id": None},
    }

    @classmethod
    def create_no_id(cls):
        return cls.create("no_id")

    @classmethod
    def create_no_contractor_id(cls):
        return cls.create("no_contractor_id")
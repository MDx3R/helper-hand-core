from typing import Generic
from datetime import datetime, time

from domain.models import (
    ApplicationModel,
    User, Order, OrderDetail, Reply,
    Contractee, Contractor, Admin
)
from domain.models.enums import (
    OrderStatusEnum, 
    PositionEnum, 
    GenderEnum, 
    ReplyStatusEnum, 
    RoleEnum, 
    UserStatusEnum, 
    CitizenshipEnum
)

from infrastructure.database.models import (
    Base, 
    UserBase, OrderBase, OrderDetailBase, ReplyBase,
    ContracteeBase, ContractorBase, AdminBase
)
from infrastructure.database.mappers import (
    Mapper, 
    ApplicationModelMapper, UserMapper, OrderMapper, OrderDetailMapper, ReplyMapper,
    AggregatedUserMapper, ContracteeMapper, ContractorMapper, AdminMapper
)

from tests.creators import (
    ModelBaseCreator, 
    UserCreator, OrderCreator, OrderDetailCreator, ReplyCreator, 
    AggregatedUserCreator, ContracteeCreator, ContractorCreator, AdminCreator
)
from tests.generators.base import (
    ApplicationModelTestCasesGenerator, BaseTestCasesGenerator
)

from .test_cases import (
    MAP, B, M,
    MapperTestCase,
    AggregatedUserMapperTestCase
)

user_data = {
    "user_id": 1,
    "surname": "Иванов",
    "name": "Иван",
    "patronymic": "Иванович",
    "phone_number": "+79991234567",
    "role": RoleEnum.contractee,
    "telegram_id": 123456789,
    "chat_id": 987654321,
    "status": UserStatusEnum.registered,
    "photos": ["photo1.jpg", "photo2.jpg"],
    "created_at": datetime(2024, 3, 16, 12, 0, 0),
    "updated_at": datetime(2024, 3, 16, 12, 30, 0),
}

order_data = {
    "order_id": 1,
    "contractor_id": 1,
    "about": "Требуются помощники",
    "address": "Москва, ул. Ленина",
    "admin_id": 3,
    "status": OrderStatusEnum.created,
    "created_at": datetime(2024, 3, 16, 12, 0, 0),
    "updated_at": datetime(2024, 3, 16, 12, 30, 0),
}

order_detail_data = {
    "detail_id": 1,
    "order_id": 1,
    "date": datetime(2024, 3, 20, 0, 0, 0),
    "start_at": time(10, 0),
    "end_at": time(18, 0),
    "position": PositionEnum.helper,
    "count": 5,
    "wager": 500,
    "gender": GenderEnum.male,
    "created_at": datetime(2024, 3, 16, 12, 0, 0),
    "updated_at": datetime(2024, 3, 16, 12, 30, 0),
}

reply_data = {
    "contractee_id": 1,
    "detail_id": 1,
    "wager": 450,
    "status": ReplyStatusEnum.created,
    "paid": datetime(2024, 3, 16, 16, 30, 0),
    "created_at": datetime(2024, 3, 16, 12, 0, 0),
    "updated_at": datetime(2024, 3, 16, 12, 30, 0),
}

contractee_data = user_data | {
    "role": RoleEnum.contractee,
    "birthday": datetime(1990, 5, 21),
    "height": 180,
    "gender": GenderEnum.male,
    "citizenship": CitizenshipEnum.russia,
    "positions": [PositionEnum.helper, PositionEnum.hostess],
}

contractor_data = user_data | {
    "role": RoleEnum.contractor,
    "about": "Надежный заказчик",
}

admin_data = user_data | {
    "role": RoleEnum.admin,
    "about": "Опытный администратор",
    "contractor_id": None,
} 

class MapperTestCasesGenerator(
    ApplicationModelTestCasesGenerator[MapperTestCase, M], 
    BaseTestCasesGenerator[MapperTestCase, B], 
    Generic[MAP, B, M]
):
    mapper: type[Mapper] = Mapper
    creator: type[ModelBaseCreator] = ModelBaseCreator

    @classmethod
    def _create_test_case(cls, data) -> MapperTestCase:
        return MapperTestCase(cls._get_mapper(), cls._create_base(data), cls._create_model(data))

    @classmethod
    def _get_mapper(cls) -> MAP:
        return cls.mapper  
    

class UserMapperTestCasesGenerator(MapperTestCasesGenerator[UserMapper, UserBase, User]):
    presets = {
        "default": user_data,
        "no_id": user_data | {"user_id": None},
        "no_patronymic": user_data | {"patronymic": None},
        "no_photos": user_data | {"photos": []}
    }
    mapper = UserMapper
    creator = UserCreator

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
    presets = {
        "default": order_data,
        "no_id": order_data | {"order_id": None},
        "no_admin_id": order_data | {"admin_id": None},
    }
    mapper = OrderMapper
    creator = OrderCreator

    @classmethod
    def create_no_id(cls):
        return cls.create("no_id")

    @classmethod
    def create_no_admin_id(cls):
        return cls.create("no_admin_id")


class OrderDetailMapperTestCasesGenerator(MapperTestCasesGenerator[OrderDetailMapper, OrderDetailBase, OrderDetail]):
    presets = {
        "default": order_detail_data,
        "no_id": order_detail_data | {"detail_id": None},
        "no_gender": order_detail_data | {"gender": None},
    }
    mapper = OrderDetailMapper
    creator = OrderDetailCreator

    @classmethod
    def create_no_id(cls):
        return cls.create("no_id")

    @classmethod
    def create_no_gender(cls):
        return cls.create("no_gender")


class ReplyMapperTestCasesGenerator(MapperTestCasesGenerator[ReplyMapper, ReplyBase, Reply]):
    presets = {
        "default": reply_data,
        "no_paid": reply_data | {"paid": None},
    }
    mapper = ReplyMapper
    creator = ReplyCreator

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
    def _create_test_case(cls, data) -> AggregatedUserMapperTestCase:
        return AggregatedUserMapperTestCase(
            cls._get_mapper(), cls._create_user_base(data), cls._create_base(data), cls._create_model(data)
        )

    @classmethod
    def create_different_update_time(cls) -> AggregatedUserMapperTestCase:
        data = cls.get_preset_data()
        altered_data = cls._concat_data(data, {"updated_at": datetime(2024, 3, 16, 13, 30, 0)})
        return cls._create_test_case_for_each(data, altered_data, altered_data)
    
    @classmethod
    def _create_test_case_for_each(cls, user_base, base, model) -> AggregatedUserMapperTestCase:
        return AggregatedUserMapperTestCase(
            cls._get_mapper(), cls._create_user_base(user_base), cls._create_base(base), cls._create_model(model)
        )

    @classmethod
    def create_no_id(cls):
        return cls.create("no_id")

    @classmethod
    def _get_mapper(cls) -> MAP:
        return cls.mapper 
    
    @staticmethod
    def _create_user_base(data) -> UserBase:
        return UserCreator.create_base(data)


class ContracteeMapperTestCasesGenerator(AggregatedUserMapperTestCasesGenerator[ContracteeMapper, ContracteeBase, Contractee]):
    presets = {
        "default": contractee_data,
        "no_id": contractee_data | {"contractee_id": None},
    }
    mapper = ContracteeMapper
    creator = ContracteeCreator


class ContractorMapperTestCasesGenerator(AggregatedUserMapperTestCasesGenerator[ContractorMapper, ContractorBase, Contractor]):
    presets = {
        "default": contractor_data,
        "no_id": contractor_data | {"contractor_id": None},
    }
    mapper = ContractorMapper
    creator = ContractorCreator


class AdminMapperTestCasesGenerator(AggregatedUserMapperTestCasesGenerator[AdminMapper, AdminBase, Admin]):
    presets = {
        "default": admin_data,
        "no_id": admin_data | {"admin_id": None},
        "no_contractor_id": admin_data | {"contractor_id": None},
    }
    mapper = AdminMapper
    creator = AdminCreator

    @classmethod
    def create_no_contractor_id(cls):
        return cls.create("no_contractor_id")
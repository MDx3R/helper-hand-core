from typing import Generic, TypeVar, Tuple, List
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
    BaseMapper, 
    ApplicationModelMapper, UserMapper, OrderMapper, OrderDetailMapper, ReplyMapper,
    AggregatedUserMapper, ContracteeMapper, ContractorMapper, AdminMapper
)

from tests.creators import (
    BaseCreator, 
    UserCreator, OrderCreator, OrderDetailCreator, ReplyCreator, 
    AggregatedUserCreator, ContracteeCreator, ContractorCreator, AdminCreator
)
from tests.base_generators import ApplicationModelTestCasesGenerator

M = TypeVar("B", bound=BaseMapper)
B = TypeVar("B", bound=Base)
AM = TypeVar("AM", bound=ApplicationModel)
UM = TypeVar("UM", ContracteeMapper, ContractorMapper, AdminMapper)
UB = TypeVar("UB", ContracteeBase, ContractorBase, AdminBase)
UAM = TypeVar("UAM", Contractee, Contractor, Admin)

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
    "admin_id": None,
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
    "gender": None,
    "created_at": datetime(2024, 3, 16, 12, 0, 0),
    "updated_at": datetime(2024, 3, 16, 12, 30, 0),
}

reply_data = {
    "contractee_id": 1,
    "detail_id": 1,
    "wager": 450,
    "status": ReplyStatusEnum.created,
    "paid": None,
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
    
class MapperTestCasesGenerator(ApplicationModelTestCasesGenerator[AM], Generic[AM, M, B]):
    data = {}
    mapper: type[BaseMapper] = BaseMapper
    creator: type[BaseCreator] = BaseCreator
    
    @classmethod
    def _get_mapper(cls) -> M:
        return cls.mapper
    
    @classmethod
    def _create_base(cls, data) -> AM:
        return cls.creator.create_base(data)
    
    @classmethod
    def create_default(cls, data=None, **kwargs) -> Tuple[M, B, AM]:
        if not data:
            data = cls.data
        data = cls._concat_data(data, kwargs)
        return cls._get_mapper(), cls._create_base(data), cls._create_model(data)   
    
class UserMapperTestCasesGenerator(MapperTestCasesGenerator[UserMapper, UserBase, User]):
    data = user_data
    mapper = UserMapper
    creator = UserCreator

    @classmethod
    def create_no_id(cls):
        return cls.create_default(**{"user_id": None})

    @classmethod
    def create_no_patronymic(cls):
        return cls.create_default(**{"patronymic": None})

    @classmethod
    def create_no_photos(cls):
        return cls.create_default(**{"photos": []})

class OrderMapperTestCasesGenerator(MapperTestCasesGenerator[OrderMapper, OrderBase, Order]):
    data = order_data
    mapper = OrderMapper
    creator = OrderCreator

class OrderDetailMapperTestCasesGenerator(MapperTestCasesGenerator[OrderDetailMapper, OrderDetailBase, OrderDetail]):
    data = order_detail_data
    mapper = OrderDetailMapper
    creator = OrderDetailCreator

class ReplyMapperTestCasesGenerator(MapperTestCasesGenerator[ReplyMapper, ReplyBase, Reply]):
    data = reply_data
    mapper = ReplyMapper
    creator = ReplyCreator

class AggregatedUserMapperTestCasesGenerator(MapperTestCasesGenerator[UM, UB, UAM]):
    mapper: type[AggregatedUserMapper] = AggregatedUserMapper
    creator: type[AggregatedUserCreator] = AggregatedUserCreator

    @staticmethod
    def _create_user_base(data) ->UB:
        return UserCreator.create_base(data)

    @classmethod
    def create_default(cls, data=None, **kwargs) -> Tuple[M, B, AM]:
        if not data:
            data = cls.data
        data = cls._concat_data(data, kwargs)
        return cls._get_mapper(), cls._create_user_base(data), cls._create_base(data), cls._create_model(data)

    @classmethod
    def create_different_update_time(cls) -> Tuple[M, B, AM]:
        data = cls._concat_data(cls.data, {"updated_at": datetime(2024, 3, 16, 13, 30, 0)})
        return cls._get_mapper(), cls._create_user_base(cls.data), cls._create_base(data), cls._create_model(data)

class ContracteeMapperTestCasesGenerator(AggregatedUserMapperTestCasesGenerator[ContracteeMapper, ContracteeBase, Contractee]):
    data = contractee_data
    mapper = ContracteeMapper
    creator = ContracteeCreator

class ContractorMapperTestCasesGenerator(AggregatedUserMapperTestCasesGenerator[ContractorMapper, ContractorBase, Contractor]):
    data = contractor_data
    mapper = ContractorMapper
    creator = ContractorCreator

class AdminMapperTestCasesGenerator(AggregatedUserMapperTestCasesGenerator[AdminMapper, AdminBase, Admin]):
    data = admin_data
    mapper = AdminMapper
    creator = AdminCreator
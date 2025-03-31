from typing import Generic, TypeVar, List, Tuple, Dict, Any
from datetime import datetime, time, date
from abc import ABC, abstractmethod
from faker import Faker
from domain.entities import ApplicationModel, User, Order, OrderDetail, Reply, Contractee, Contractor, Admin
from infrastructure.database.models import Base, UserBase, OrderBase, OrderDetailBase, ReplyBase, ContracteeBase, ContractorBase, AdminBase

from domain.entities.enums import (
    OrderStatusEnum, 
    PositionEnum, 
    GenderEnum, 
    ReplyStatusEnum, 
    RoleEnum, 
    UserStatusEnum, 
    CitizenshipEnum
)

fk = Faker("ru_RU")

B = TypeVar("B", bound=Base)
M = TypeVar("M", bound=ApplicationModel)

class ModelBaseFactory(ABC, Generic[B, M]):
    model: type[ApplicationModel] = ApplicationModel
    base: type[Base] = Base
    fixed_data = {}

    @classmethod
    def _create_model(cls, data: Dict[str, Any]) -> M:
        return cls.model.model_validate(data)

    @classmethod
    def _create_base(cls, data: Dict[str, Any]) -> B:
        return cls.base.base_validate(data)

    @classmethod
    def create_model(cls, **kwargs) -> M:
        return cls._create_model(cls.fixed_data | kwargs)

    @classmethod
    def create_base(cls, **kwargs) -> B:
        return cls._create_base(cls.fixed_data | kwargs)

    @classmethod
    def create_random_model(cls, **kwargs) -> M:
        return cls._create_model(cls.get_random_data(**kwargs))

    @classmethod
    def create_random_base(cls, **kwargs) -> B:
        return cls._create_base(cls.get_random_data(**kwargs))

    @classmethod
    def get_random_model_list(cls, _count: int = 3, **kwargs) -> List[M]:
        return [cls.create_random_model(**kwargs) for _ in range(_count)]
    
    @classmethod
    def get_random_base_list(cls, _count: int = 3, **kwargs) -> List[B]:
        return [cls.create_random_base(**kwargs) for _ in range(_count)]

    @classmethod
    def get_pair_list(cls, _count: int = 3, _random: bool = False, **kwargs) -> List[Tuple[B, M]]:
        method = cls.get_random_pair if _random else cls.get_default_pair
        return [method(**kwargs) for _ in range(_count)]

    @classmethod
    def get_default_pair(cls, **kwargs) -> Tuple[B, M]:
        data = cls.get_default_data(**kwargs)
        base = cls._create_base(data)
        model = cls._create_model(data)
        return base, model

    @classmethod
    def get_random_pair(cls, **kwargs) -> Tuple[B, M]:
        data = cls.get_random_data(**kwargs)
        base = cls._create_base(data)
        model = cls._create_model(data)
        return base, model

    @classmethod
    def get_default_data(cls, **kwargs) -> Dict[str, Any]:
        return cls.fixed_data | kwargs

    @classmethod
    @abstractmethod
    def get_random_data(cls, **kwargs) -> Dict[str, Any]:
        pass

class UserFactory(ModelBaseFactory[UserBase, User]):
    model = User
    base = UserBase
    fixed_data = {
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

    @classmethod
    def get_random_data(cls, **kwargs) -> Dict[str, Any]:
        return {
            "user_id": fk.unique.random_int(min=1, max=1000),
            "surname": fk.last_name(),
            "name": fk.first_name(),
            "patronymic": fk.middle_name(),
            "phone_number": fk.unique.phone_number(),
            "role": RoleEnum.contractee,
            "telegram_id": fk.unique.random_int(min=100000, max=999999999),
            "chat_id": fk.unique.random_int(min=100000, max=999999999),
            "status": fk.random_element(elements=[e for e in UserStatusEnum]),
            "photos": [fk.image_url() for _ in range(2)],
            "created_at": fk.date_time_this_year(),
            "updated_at": fk.date_time_this_year(),
        } | kwargs


class OrderFactory(ModelBaseFactory[OrderBase, Order]):
    model = Order
    base = OrderBase
    fixed_data = {
        "order_id": 1,
        "contractor_id": 1,
        "about": "Требуются помощники",
        "address": "Москва, ул. Ленина",
        "admin_id": None,
        "status": OrderStatusEnum.created,
        "created_at": datetime(2024, 3, 16, 12, 0, 0),
        "updated_at": datetime(2024, 3, 16, 12, 30, 0),
    }

    @classmethod
    def get_random_data(cls, **kwargs) -> Dict[str, Any]:
        return {
            "order_id": fk.unique.random_int(min=1, max=1000),
            "contractor_id": fk.random_int(min=1, max=100),
            "about": fk.sentence(),
            "address": fk.address(),
            "admin_id": fk.random_element(elements=[None, fk.random_int(min=1, max=100)]),
            "status": fk.random_element(elements=[e for e in OrderStatusEnum]),
            "created_at": fk.date_time_this_year(),
            "updated_at": fk.date_time_this_year(),
        } | kwargs

class OrderDetailFactory(ModelBaseFactory[OrderDetailBase, OrderDetail]):
    model = OrderDetail
    base = OrderDetailBase
    fixed_data = {
        "detail_id": 1,
        "order_id": 1,
        "date": date(2024, 3, 20),
        "start_at": time(10, 0),
        "end_at": time(18, 0),
        "position": PositionEnum.helper,
        "count": 5,
        "wager": 500,
        "gender": None,
        "created_at": datetime(2024, 3, 16, 12, 0, 0),
        "updated_at": datetime(2024, 3, 16, 12, 30, 0),
    }

    @classmethod
    def get_random_data(cls, **kwargs) -> Dict[str, Any]:
        return {
            "detail_id": fk.unique.random_int(min=1, max=1000),
            "order_id": fk.random_int(min=1, max=100),
            "date": fk.date_this_year(),
            "start_at": fk.time_object(),
            "end_at": fk.time_object(),
            "position": fk.random_element(elements=[e for e in PositionEnum]),
            "count": fk.random_int(min=1, max=10),
            "wager": fk.random_int(min=100, max=1000),
            "gender": fk.random_element(elements=[e for e in GenderEnum] + [None]),
            "created_at": fk.date_time_this_year(),
            "updated_at": fk.date_time_this_year(),
        } | kwargs

class ReplyFactory(ModelBaseFactory[ReplyBase, Reply]):
    model = Reply
    base = ReplyBase
    fixed_data = {
        "contractee_id": 1,
        "detail_id": 1,
        "wager": 450,
        "status": ReplyStatusEnum.created,
        "paid": None,
        "created_at": datetime(2024, 3, 16, 12, 0, 0),
        "updated_at": datetime(2024, 3, 16, 12, 30, 0),
    }

    @classmethod
    def get_random_data(cls, **kwargs) -> Dict[str, Any]:
        return {
            "contractee_id": fk.random_int(min=1, max=100),
            "detail_id": fk.random_int(min=1, max=100),
            "wager": fk.random_int(min=100, max=1000),
            "status": fk.random_element(elements=[e for e in ReplyStatusEnum]),
            "paid": fk.random_element(elements=[None, fk.date_time_this_year()]),
            "created_at": fk.date_time_this_year(),
            "updated_at": fk.date_time_this_year(),
        } | kwargs


class AggregatedUserFactory(ModelBaseFactory[B, M]):
    role_id_field: str = "user_id"

    @classmethod
    def _assign_user_id_to_role_id_field(cls, data: dict):
        data[cls.role_id_field] = data.get("user_id")

    @classmethod
    def _create_model(cls, data: Dict[str, Any]) -> M:
        cls._assign_user_id_to_role_id_field(data)
        return cls.model.model_validate(data)

    @classmethod
    def _create_base(cls, data: Dict[str, Any]) -> B:
        cls._assign_user_id_to_role_id_field(data)
        return cls.base.base_validate(data)
    
    @classmethod
    def _create_user_base(cls, data: Dict[str, Any]) -> UserBase:
        cls._assign_user_id_to_role_id_field(data)
        return UserFactory._create_base(data)
    
    @classmethod
    def create_user_base(cls, **kwargs) -> UserBase:
        return cls._create_user_base(cls.fixed_data | kwargs)
    
    @classmethod
    @abstractmethod
    def _get_random_data(cls, **kwargs) -> Dict[str, Any]:
        pass

    @classmethod
    def get_random_data(cls, **kwargs) -> Dict[str, Any]:
        data = cls._get_random_data(**kwargs)
        cls._assign_user_id_to_role_id_field(data)
        return data
    
    @classmethod
    def get_default_data(cls, **kwargs) -> Dict[str, Any]:
        data = super().get_default_data(**kwargs)
        cls._assign_user_id_to_role_id_field(data)
        return data

class ContracteeFactory(AggregatedUserFactory[ContracteeBase, Contractee]):
    role_id_field: str = "contractee_id"
    model = Contractee
    base = ContracteeBase
    fixed_data = UserFactory.fixed_data | {
        "role": RoleEnum.contractee,
        "birthday": date(1990, 5, 21),
        "height": 180,
        "gender": GenderEnum.male,
        "citizenship": CitizenshipEnum.russia,
        "positions": [PositionEnum.helper, PositionEnum.hostess],
    }

    @classmethod
    def _get_random_data(cls, **kwargs) -> Dict[str, Any]:
        return UserFactory.get_random_data() | {
            "role": RoleEnum.contractee,
            "birthday": fk.date_of_birth(minimum_age=18, maximum_age=60),
            "height": fk.random_int(min=150, max=200),
            "gender": fk.random_element(elements=[e for e in GenderEnum]),
            "citizenship": fk.random_element(elements=[e for e in CitizenshipEnum]),
            "positions": fk.random_elements(elements=[e for e in PositionEnum], length=2),
        } | kwargs

class ContractorFactory(AggregatedUserFactory[ContractorBase, Contractor]):
    role_id_field: str = "contractor_id"
    model = Contractor
    base = ContractorBase
    fixed_data = UserFactory.fixed_data | {
        "role": RoleEnum.contractor,
        "about": "Надежный заказчик",
    }

    @classmethod
    def _get_random_data(cls, **kwargs) -> Dict[str, Any]:
        return UserFactory.get_random_data() | {
            "role": RoleEnum.contractor,
            "about": fk.paragraph(),
        } | kwargs

class AdminFactory(AggregatedUserFactory[AdminBase, Admin]):
    role_id_field: str = "admin_id"
    model = Admin
    base = AdminBase
    fixed_data = UserFactory.fixed_data | {
        "role": RoleEnum.admin,
        "about": "Опытный администратор",
        "contractor_id": None,
    }

    @classmethod
    def _get_random_data(cls, **kwargs) -> Dict[str, Any]:
        return UserFactory.get_random_data() | {
            "role": RoleEnum.admin,
            "about": fk.paragraph(),
            "contractor_id": fk.random_element(elements=[None, fk.random_int(min=1, max=100)]),
        } | kwargs
from typing import Generic, TypeVar
from domain.models import ApplicationModel, User, Order, OrderDetail, Reply, Contractee, Contractor, Admin
from infrastructure.database.models import Base, UserBase, OrderBase, OrderDetailBase, ReplyBase, ContracteeBase, ContractorBase, AdminBase

B = TypeVar("B", bound=Base)
M = TypeVar("M", bound=ApplicationModel)
UB = TypeVar("B", ContracteeBase, ContractorBase, AdminBase)
UM = TypeVar("M", Contractee, Contractor, Admin)

class BaseCreator(Generic[B, M]):
    model: type[ApplicationModel] = ApplicationModel
    base: type[Base] = Base

    @classmethod
    def create_model(cls, data) -> M:
        return cls.model.model_validate(data)

    @classmethod
    def create_base(cls, data) -> B:
        return cls.base.base_validate(data)

class UserCreator(BaseCreator[UserBase, User]):
    model = User
    base = UserBase

class OrderCreator(BaseCreator[OrderBase, Order]):
    model = Order
    base = OrderBase

class OrderDetailCreator(BaseCreator[OrderDetailBase, OrderDetail]):
    model = OrderDetail
    base = OrderDetailBase

class ReplyCreator(BaseCreator[ReplyBase, Reply]):
    model = Reply
    base = ReplyBase

class AggregatedUserCreator(BaseCreator[UB, UM]):
    role_id_field: str = "user_id"

    @classmethod
    def assign_user_id_to_role_id_field(cls, data: dict):
        data[cls.role_id_field] = data.get("user_id")

    @classmethod
    def create_model(cls, data) -> M:
        cls.assign_user_id_to_role_id_field(data)
        return cls.model.model_validate(data)

    @classmethod
    def create_base(cls, data) -> B:
        cls.assign_user_id_to_role_id_field(data)
        return cls.base.base_validate(data)

class ContracteeCreator(AggregatedUserCreator[ContracteeBase, Contractee]):
    role_id_field: str = "contractee_id"
    model = Contractee
    base = ContracteeBase

class ContractorCreator(AggregatedUserCreator[ContractorBase, Contractor]):
    role_id_field: str = "contractee_id"
    model = Contractor
    base = ContractorBase

class AdminCreator(AggregatedUserCreator[AdminBase, Admin]):
    role_id_field: str = "admin_id"
    model = Admin
    base = AdminBase
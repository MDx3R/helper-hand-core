from typing import Type, TypeVar, List, Tuple, Union, Any, Generic
from abc import ABC, abstractmethod

from domain.models import (
    ApplicationModel, 
    User, Admin, Contractee, Contractor,
    Order, OrderDetail, DetailedOrder,
    Reply, DetailedReply
)

from infrastructure.database.models import (
    Base, 
    UserBase, AdminBase, ContracteeBase, ContractorBase,
    OrderBase, OrderDetailBase,
    ReplyBase
)

B = TypeVar("B", bound=Base)
M = TypeVar("M", bound=ApplicationModel)

UB = TypeVar("UB", ContracteeBase, ContractorBase, AdminBase)
UM = TypeVar("UM", Contractee, Contractor, Admin)

class MapperRegistry:
    def __init__(self, mapping: dict[type[Base], type[ApplicationModel]]):
        self.mapping = mapping

    def get_model(self, base_type: type[Base]) -> type[ApplicationModel]:
        model_type = self.mapping.get(base_type)
        if not model_type:
            raise TypeError(f"Отсутствует соответствие между `{base_type}` и моделью")
        return model_type

    def get_base(self, model_type: type[ApplicationModel]) -> type[Base]:
        base_type = next((k for k, v in self.mapping.items() if v == model_type), None)
        if not base_type:
            raise TypeError(f"Отсутствует соответствие между `{model_type}` и моделью SQLAlchemy")
        return base_type


class BaseMapper(ABC):
    registry = MapperRegistry()

    @classmethod
    def _map_model_type_to_base(cls, model_type: type[ApplicationModel]) -> type[Base]:
        return cls.registry.get_base(model_type)

    @classmethod
    def _map_base_type_to_model(cls, base_type: type[Base]) -> type[ApplicationModel]:
        return cls.registry.get_model(base_type)

    @classmethod
    def _filter_fields(cls, data: dict[str, Any], exclude: set[str]) -> dict[str, Any]:
        return {k: v for k, v in data.items() if k in exclude}

    @classmethod
    def _base_to_model(cls, base: Base) -> ApplicationModel:
        data = base.get_fields()
        model = cls._map_base_type_to_model(type(base))
        return model.model_validate(data) # Pydantic-модели позволяют передавать лишние аргументы

    @classmethod
    def _model_to_base(cls, model: ApplicationModel) -> Base:
        data = model.get_fields()
        base_type = cls._map_model_type_to_base(type(model))
        return base_type.base_validate(data) # Base-модели позволяют передавать лишние аргументы


class ApplicationModelMapper(BaseMapper, Generic[B, M]):
    registry = MapperRegistry({
        UserBase: User,
        OrderBase: Order,
        OrderDetailBase: OrderDetail,
        ReplyBase: Reply,
    })

    @classmethod
    def to_model(cls, base: B) -> M:
        """Конвертирует SQLAlchemy-модель в модель приложения."""
        return cls._base_to_model(base)
    
    @classmethod
    def to_base(cls, model: M) -> B:
        """Конвертирует модель приложения в SQLAlchemy-модель."""
        return cls._model_to_base(model)


class UserMapper(ApplicationModelMapper[UserBase, User]):
    pass

 
class OrderMapper(ApplicationModelMapper[OrderBase, Order]):
    pass


class OrderDetailMapper(ApplicationModelMapper[OrderDetailBase, OrderDetail]):
    pass


class ReplyMapper(ApplicationModelMapper[ReplyBase, Reply]):
    pass


class AggregatedUserMapper(BaseMapper, Generic[UB, UM]):
    registry = MapperRegistry({
        ContracteeBase: Contractee,
        ContractorBase: Contractor,
        AdminBase: Admin,
    })

    @classmethod
    def to_model(cls, user: UserBase, role: UB) -> UM:
        user_data = user.get_fields()
        role_data = cls._filter_fields(role.get_fields(), {"created_at", "updated_at"})

        model = cls.registry.get_model(type(role))
        return model(**user_data, **role_data)
    
    @classmethod
    def to_base(cls, model: UM) -> UB:
        return cls._model_to_base(model)
    
    @classmethod
    def to_user_base(cls, model: UM) -> UB:
        user = User(model.get_fields())
        return UserMapper.to_base(user)


class ContracteeMapper(AggregatedUserMapper[ContracteeBase, Contractee]):
    pass
    

class ContractorMapper(AggregatedUserMapper[ContractorBase, Contractor]):
    pass
    

class AdminMapper(AggregatedUserMapper[AdminBase, Admin]):
    pass


class DetailedOrderMapper(BaseMapper):
    @classmethod
    def to_model(cls, order: OrderBase, details: List[OrderDetailBase]) -> DetailedOrder:
        order_data = OrderMapper.to_model(order).get_fields()
        return DetailedOrder(
            **order_data, 
            details=[OrderDetailMapper.to_model(detail) for detail in details]
        )
    
    @classmethod
    def to_base(cls, detailed_order: DetailedOrder) -> Tuple[OrderBase, List[OrderDetailBase]]:
        return (
            cls.to_order_base(detailed_order), 
            [OrderDetailMapper.to_base(detail) for detail in detailed_order]
        )
    
    @classmethod
    def to_order_base(cls, model: DetailedOrder) -> OrderBase:
        order = Order(model.get_fields())
        return OrderMapper.to_base(order)
    

class DetailedReplyMapper(BaseMapper):
    @classmethod
    def to_model(
        cls, 
        reply: ReplyBase, 
        user: UserBase, 
        contractee: ContracteeBase, 
        detail: OrderDetailBase, 
        order: OrderBase
    ) -> DetailedReply:
        reply_data = ReplyMapper.to_model(reply).get_fields()
        return DetailedReply(
            **reply_data,
            contractee=ContracteeMapper.to_model(user, contractee),
            detail=OrderDetailMapper.to_model(detail),
            order=OrderMapper.to_model(order),
        )
    
    @classmethod
    def to_base(
        cls, detailed_reply: DetailedReply
    ) -> Tuple[ReplyBase, UserBase, ContracteeBase, OrderDetailBase, OrderBase]:
        return (
            cls.to_reply_base(detailed_reply),
            ContracteeMapper.to_user_base(detailed_reply.contractee),
            ContracteeMapper.to_base(detailed_reply.contractee),
            OrderDetailMapper.to_base(detailed_reply.detail),
            OrderMapper.to_base(detailed_reply.order)
        )
    
    @classmethod
    def to_reply_base(cls, model: DetailedReply) -> ReplyBase:
        reply = Reply(model.get_fields())
        return OrderMapper.to_base(reply)
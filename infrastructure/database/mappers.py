from typing import Type, TypeVar, List, Tuple, Union, Any, Generic
from abc import ABC, abstractmethod

from domain.entities import (
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
    def __init__(self, mapping: dict[type[Base], type[ApplicationModel]] = {}):
        self.mapping = mapping

    def get_model(self, base_type: type[Base]) -> type[ApplicationModel]:
        model_type = self.mapping.get(base_type)
        if not model_type:
            raise TypeError(f"Отсутствует соответствие между `{base_type.__name__}` и моделью")
        return model_type

    def get_base(self, model_type: type[ApplicationModel]) -> type[Base]:
        base_type = next((k for k, v in self.mapping.items() if v == model_type), None)
        if not base_type:
            raise TypeError(f"Отсутствует соответствие между `{model_type.__name__}` и моделью SQLAlchemy")
        return base_type


class Mapper(ABC):
    registry = MapperRegistry()

    @classmethod
    def _map_model_type_to_base(cls, model_type: type[ApplicationModel]) -> type[Base]:
        return cls.registry.get_base(model_type)

    @classmethod
    def _map_base_type_to_model(cls, base_type: type[Base]) -> type[ApplicationModel]:
        return cls.registry.get_model(base_type)

    @classmethod
    def _filter_fields(cls, data: dict[str, Any], exclude: set[str]) -> dict[str, Any]:
        return {k: v for k, v in data.items() if k not in exclude}

    @classmethod
    def _base_to_model(cls, base: Base) -> ApplicationModel:
        model = cls._map_base_type_to_model(type(base))
        data = base.get_fields()
        return model.model_validate(data) # Pydantic-модели позволяют передавать лишние аргументы

    @classmethod
    def _model_to_base(cls, model: ApplicationModel) -> Base:
        base_type = cls._map_model_type_to_base(type(model))
        data = model.get_fields()
        return base_type.base_validate(data) # Base-модели позволяют передавать лишние аргументы


class ApplicationModelMapper(Mapper, Generic[B, M]):
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

    @classmethod
    def to_model_list(cls, bases: List[B]) -> List[M]:
        """Конвертирует список SQLAlchemy-моделей в список моделей приложения."""
        return [cls.to_model(base) for base in bases]

    @classmethod
    def to_base_list(cls, models: List[M]) -> List[B]:
        """Конвертирует список моделей приложения в список SQLAlchemy-моделей."""
        return [cls.to_base(model) for model in models]

class UserMapper(ApplicationModelMapper[UserBase, User]):
    pass

 
class OrderMapper(ApplicationModelMapper[OrderBase, Order]):
    pass


class OrderDetailMapper(ApplicationModelMapper[OrderDetailBase, OrderDetail]):
    pass


class ReplyMapper(ApplicationModelMapper[ReplyBase, Reply]):
    pass


class AggregatedUserMapper(Mapper, Generic[UB, UM]):
    registry = MapperRegistry({
        ContracteeBase: Contractee,
        ContractorBase: Contractor,
        AdminBase: Admin,
    })

    @classmethod
    def to_model(cls, user: UserBase, role: UB) -> UM:
        """Конвертирует SQLAlchemy-модель пользователя и его роли в модель приложения."""
        user_data = cls._filter_fields(user.get_fields(), {"created_at", "updated_at"})
        role_data = role.get_fields()

        model = cls.registry.get_model(type(role))
        return model(**user_data, **role_data)
    
    @classmethod
    def to_base(cls, model: UM) -> Tuple[UserBase, UB]:
        """Конвертирует модель приложения в SQLAlchemy-модель пользователя и его роли."""
        return cls.to_user_base(model), cls.to_role_base(model)
    
    @classmethod
    def to_user_base(cls, model: UM) -> UserBase:
        """Конвертирует модель приложения в SQLAlchemy-модель пользователя."""
        user = User.model_validate(model.get_fields())
        return UserMapper.to_base(user)
    
    @classmethod
    def to_role_base(cls, model: UM) -> UB:
        """Конвертирует модель приложения в SQLAlchemy-модель роли пользователя."""
        return cls._model_to_base(model)
    
    @classmethod
    def to_model_list(cls, bases: List[Tuple[UserBase, UB]]) -> List[UM]:
        """Конвертирует список SQLAlchemy-моделей пользователя и его роли в список моделей приложения."""
        return [cls.to_model(user, role) for user, role in bases]

    @classmethod
    def to_base_list(cls, models: List[UM]) -> List[Tuple[UserBase, UB]]:
        """Конвертирует список моделей приложения в список SQLAlchemy-моделей пользователя и его роли."""
        return [cls.to_base(model) for model in models]


class ContracteeMapper(AggregatedUserMapper[ContracteeBase, Contractee]):
    pass
    

class ContractorMapper(AggregatedUserMapper[ContractorBase, Contractor]):
    pass
    

class AdminMapper(AggregatedUserMapper[AdminBase, Admin]):
    pass


class DetailedOrderMapper(Mapper):
    @classmethod
    def to_model(cls, order: OrderBase, details: List[OrderDetailBase]) -> DetailedOrder:
        """Конвертирует SQLAlchemy-модель заказа и его сведений в модель приложения."""
        order_data = OrderMapper.to_model(order).get_fields()
        return DetailedOrder(
            **order_data, 
            details=[OrderDetailMapper.to_model(detail) for detail in details]
        )
    
    @classmethod
    def to_base(cls, detailed_order: DetailedOrder) -> Tuple[OrderBase, List[OrderDetailBase]]:
        """Конвертирует модель приложения в SQLAlchemy-модель заказа и его сведений."""
        return (
            cls.to_order_base(detailed_order), 
            [OrderDetailMapper.to_base(detail) for detail in detailed_order]
        )
    
    @classmethod
    def to_order_base(cls, model: DetailedOrder) -> OrderBase:
        """Конвертирует модель приложения в SQLAlchemy-модель заказа."""
        order = Order.model_validate(model.get_fields())
        return OrderMapper.to_base(order)
    
    @classmethod
    def to_model_list(cls, bases: List[Tuple[OrderBase, List[OrderDetailBase]]]) -> List[DetailedOrder]:
        """Конвертирует список SQLAlchemy-моделей заказа и его сведений в список моделей приложения."""
        return [cls.to_model(order, details) for order, details in bases]

    @classmethod
    def to_base_list(cls, models: List[DetailedOrder]) -> List[Tuple[OrderBase, List[OrderDetailBase]]]:
        """Конвертирует список моделей приложения в список SQLAlchemy-моделей пользователя и его роли."""
        return [cls.to_base(model) for model in models]
    

class DetailedReplyMapper(Mapper):
    @classmethod
    def to_model(
        cls, 
        reply: ReplyBase, 
        user: UserBase, 
        contractee: ContracteeBase, 
        detail: OrderDetailBase, 
        order: OrderBase
    ) -> DetailedReply:
        """Конвертирует SQLAlchemy-модель отклика, пользователя и исполнителя, сведений и заказа и его сведений в модель приложения."""
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
        """Конвертирует модель приложения в SQLAlchemy-модель отклика, пользователя и исполнителя, сведений и заказа."""
        return (
            cls.to_reply_base(detailed_reply),
            ContracteeMapper.to_user_base(detailed_reply.contractee),
            ContracteeMapper.to_base(detailed_reply.contractee),
            OrderDetailMapper.to_base(detailed_reply.detail),
            OrderMapper.to_base(detailed_reply.order)
        )
    
    @classmethod
    def to_reply_base(cls, model: DetailedReply) -> ReplyBase:
        """Конвертирует модель приложения в SQLAlchemy-модель отклика."""
        reply = Reply.model_validate(model.get_fields())
        return OrderMapper.to_base(reply)
    
    @classmethod
    def to_model_list(cls, bases: List[Tuple[ReplyBase, UserBase, ContracteeBase, OrderDetailBase, OrderBase]]) -> List[DetailedReply]:
        """Конвертирует список SQLAlchemy-моделей заказа и его сведений в список моделей приложения."""
        return [cls.to_model(*base) for base in bases]

    @classmethod
    def to_base_list(cls, models: List[DetailedReply]) -> List[Tuple[ReplyBase, UserBase, ContracteeBase, OrderDetailBase, OrderBase]]:
        """Конвертирует список моделей приложения в список SQLAlchemy-моделей пользователя и его роли."""
        return [cls.to_base(model) for model in models]
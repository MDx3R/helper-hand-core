from re import L
from typing import Optional, Type, TypeVar, List, Tuple, Union, Any, Generic
from abc import ABC, abstractmethod

from domain.entities.base import ApplicationModel
from domain.entities.order.detail import OrderDetail
from domain.entities.order.order import Order
from domain.entities.reply.composite_reply import (
    CompleteReply,
    ReplyWithDetail,
)
from domain.entities.reply.reply import Reply
from domain.entities.token.token import Token
from domain.entities.user.admin.admin import Admin
from domain.entities.user.admin.composite_admin import CompleteAdmin
from domain.entities.user.contractee.composite_contractee import (
    CompleteContractee,
)
from domain.entities.user.contractee.contractee import Contractee
from domain.entities.user.contractor.composite_contractor import (
    CompleteContractor,
)
from domain.entities.user.contractor.contractor import Contractor
from domain.entities.user.credentials import (
    TelegramCredentials,
    UserCredentials,
    WebCredentials,
)
from domain.entities.user.enums import RoleEnum
from domain.entities.user.user import User
from infrastructure.database.models import (
    Base,
    TelegramCredentialsBase,
    TokenBase,
    UserBase,
    AdminBase,
    ContracteeBase,
    ContractorBase,
    OrderBase,
    OrderDetailBase,
    ReplyBase,
    WebCredentialsBase,
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
            raise TypeError(
                f"Отсутствует соответствие между `{base_type.__name__}` и моделью"
            )
        return model_type

    def get_base(self, model_type: type[ApplicationModel]) -> type[Base]:
        base_type = next(
            (k for k, v in self.mapping.items() if v == model_type), None
        )
        if not base_type:
            raise TypeError(
                f"Отсутствует соответствие между `{model_type.__name__}` и моделью SQLAlchemy"
            )
        return base_type


class Mapper(ABC):
    registry = MapperRegistry()

    @classmethod
    def _map_model_type_to_base(
        cls, model_type: type[ApplicationModel]
    ) -> type[Base]:
        return cls.registry.get_base(model_type)

    @classmethod
    def _map_base_type_to_model(
        cls, base_type: type[Base]
    ) -> type[ApplicationModel]:
        return cls.registry.get_model(base_type)

    @classmethod
    def _filter_fields(
        cls, data: dict[str, Any], exclude: set[str]
    ) -> dict[str, Any]:
        return {k: v for k, v in data.items() if k not in exclude}

    @classmethod
    def _base_to_model(cls, base: Base) -> ApplicationModel:
        model = cls._map_base_type_to_model(type(base))
        data = base.get_fields()
        return model.model_validate(
            data
        )  # Pydantic-модели позволяют передавать лишние аргументы

    @classmethod
    def _model_to_base(cls, model: ApplicationModel) -> Base:
        base_type = cls._map_model_type_to_base(type(model))
        data = model.get_fields()
        return base_type.base_validate(
            data
        )  # Base-модели позволяют передавать лишние аргументы


class ApplicationModelMapper(Mapper, Generic[B, M]):
    registry = MapperRegistry(
        {
            UserBase: User,
            OrderBase: Order,
            OrderDetailBase: OrderDetail,
            ReplyBase: Reply,
            TelegramCredentialsBase: TelegramCredentials,
            WebCredentialsBase: WebCredentials,
            TokenBase: Token,
        }
    )

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


class TelegramCredentialsMapper(
    ApplicationModelMapper[TelegramCredentialsBase, TelegramCredentials]
):
    pass


class WebCredentialsMapper(
    ApplicationModelMapper[WebCredentialsBase, WebCredentials]
):
    pass


class TokenMapper(ApplicationModelMapper[TokenBase, Token]):
    pass


class UserCredentialsMapper:
    @classmethod
    def to_model(
        cls,
        web_base: Optional[WebCredentialsBase],
        tg_base: Optional[TelegramCredentialsBase],
    ) -> UserCredentials:
        web = WebCredentialsMapper.to_model(web_base) if web_base else None
        telegram = (
            TelegramCredentialsMapper.to_model(tg_base) if tg_base else None
        )
        return UserCredentials(telegram=telegram, web=web)

    @classmethod
    def to_base(
        cls,
        web: Optional[WebCredentials],
        tg: Optional[TelegramCredentials],
    ) -> Tuple[
        Optional[WebCredentialsBase], Optional[TelegramCredentialsBase]
    ]:
        web_base = WebCredentialsMapper.to_base(web) if web else None
        tg_base = TelegramCredentialsMapper.to_base(tg) if tg else None
        return web_base, tg_base


class AggregatedUserMapper(Mapper, Generic[UB, UM]):
    registry = MapperRegistry(
        {
            ContracteeBase: Contractee,
            ContractorBase: Contractor,
            AdminBase: Admin,
        }
    )

    @classmethod
    def to_model(cls, user: UserBase, role: UB) -> UM:
        """Конвертирует SQLAlchemy-модель пользователя и его роли в модель приложения."""
        user_data = cls._filter_fields(
            user.get_fields(), {"created_at", "updated_at"}
        )
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


class CompleteAdminMapper:
    @classmethod
    def to_model(
        cls,
        user: UserBase,
        admin: AdminBase,
        contractor: Optional[ContractorBase],
        web: Optional[WebCredentialsBase],
        telegram: Optional[TelegramCredentialsBase],
    ) -> CompleteAdmin:
        return CompleteAdmin(
            user=AdminMapper.to_model(user, admin),
            contractor=(
                ContractorMapper.to_model(user, contractor)
                if contractor
                else None
            ),
            credentials=UserCredentialsMapper.to_model(web, telegram),
        )


class CompleteContractorMapper:
    @classmethod
    def to_model(
        cls,
        user: UserBase,
        contractor: ContractorBase,
        web: Optional[WebCredentialsBase],
        telegram: Optional[TelegramCredentialsBase],
    ) -> CompleteContractor:
        return CompleteContractor(
            user=ContractorMapper.to_model(user, contractor),
            credentials=UserCredentialsMapper.to_model(web, telegram),
        )


class CompleteContracteeMapper:
    @classmethod
    def to_model(
        cls,
        user: UserBase,
        contractee: ContracteeBase,
        web: Optional[WebCredentialsBase],
        telegram: Optional[TelegramCredentialsBase],
    ) -> CompleteContractee:
        return CompleteContractee(
            user=ContracteeMapper.to_model(user, contractee),
            credentials=UserCredentialsMapper.to_model(web, telegram),
        )


class CompleteRoleMapper:
    mapping: dict[RoleEnum, Any] = {
        RoleEnum.admin: CompleteAdminMapper,
        RoleEnum.contractor: CompleteContractorMapper,
        RoleEnum.contractee: CompleteContracteeMapper,
    }

    @classmethod
    def to_model(
        cls,
        user: UserBase,
        admin: Optional[AdminBase],
        contractor: Optional[ContractorBase],
        contractee: Optional[ContracteeBase],
        web: Optional[WebCredentialsBase],
        telegram: Optional[TelegramCredentialsBase],
    ) -> CompleteAdmin | CompleteContractor | CompleteContractee:
        if not (admin or contractor or contractee):
            raise ValueError(f"Отсутсвует роль: {user.role}")
        match user.role:
            case RoleEnum.admin:
                return CompleteAdminMapper.to_model(
                    user=user,
                    admin=admin,
                    contractor=contractor,
                    web=web,
                    telegram=telegram,
                )
            case RoleEnum.contractor:
                return CompleteContractorMapper.to_model(
                    user=user,
                    contractor=contractor,
                    web=web,
                    telegram=telegram,
                )
            case RoleEnum.contractee:
                return CompleteContracteeMapper.to_model(
                    user=user,
                    contractee=contractee,
                    web=web,
                    telegram=telegram,
                )
            case _:
                raise ValueError(f"Неподдерживаемая роль: {user.role}")


class ReplyWithDetailMapper:
    @classmethod
    def to_model(
        cls,
        reply: ReplyBase,
        detail: OrderDetailBase,
    ) -> ReplyWithDetail:
        return ReplyWithDetail(
            reply=ReplyMapper.to_model(reply),
            detail=OrderDetailMapper.to_model(detail),
        )


class CompleteReplyMapper:
    @classmethod
    def to_model(
        cls,
        reply: ReplyBase,
        contractee_user: UserBase,
        contractee: ContracteeBase,
        detail: OrderDetailBase,
        order: OrderBase,
    ) -> CompleteReply:
        return CompleteReply(
            reply=ReplyMapper.to_model(reply),
            contractee=ContracteeMapper.to_model(contractee_user, contractee),
            detail=OrderDetailMapper.to_model(detail),
            order=OrderMapper.to_model(order),
        )

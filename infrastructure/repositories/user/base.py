from typing import Generic, Optional, Self
from sqlalchemy import Column, ColumnElement, Row, Select, asc, desc, select
from domain.dto.base import SortingOrder
from infrastructure.database.models import (
    AdminBase,
    Base,
    ContracteeBase,
    ContractorBase,
    TelegramCredentialsBase,
    UserBase,
    WebCredentialsBase,
)
from domain.dto.user.internal.user_filter_dto import (
    AdminFilterDTO,
    ContracteeFilterDTO,
    ContractorFilterDTO,
    UserFilterDTO,
)
from infrastructure.repositories.base import (
    O,
    JoinInfo,
    JoinStrategy,
    JoinType,
    UnmappedEntity,
    frozen,
    get_column_value,
)

ALIASES = {
    "user": UserBase,
    "admin": AdminBase,
    "contractor": ContractorBase,
    "contractee": ContracteeBase,
    "web": WebCredentialsBase,
    "telegram": TelegramCredentialsBase,
}


@frozen(init=False)
class UnmappedUser(UnmappedEntity):
    _aliases = ALIASES
    user: UserBase
    web: Optional[WebCredentialsBase]
    telegram: Optional[TelegramCredentialsBase]


class UserJoinStrategy(JoinStrategy):
    def __init__(self, join_type: JoinType = JoinType.INNER):
        self.join_type = join_type

    def get_strategies(self) -> dict[type[Base], JoinInfo]:
        return {
            AdminBase: JoinInfo(
                UserBase.user_id, AdminBase.admin_id, self.join_type
            ),
            ContracteeBase: JoinInfo(
                UserBase.user_id, ContracteeBase.contractee_id, self.join_type
            ),
            ContractorBase: JoinInfo(
                UserBase.user_id, ContractorBase.contractor_id, self.join_type
            ),
            WebCredentialsBase: JoinInfo(
                UserBase.user_id, WebCredentialsBase.user_id, JoinType.OUTER
            ),
            TelegramCredentialsBase: JoinInfo(
                UserBase.user_id,
                TelegramCredentialsBase.user_id,
                JoinType.OUTER,
            ),
        }


class UserOuterJoinStrategy(UserJoinStrategy):
    def __init__(self):
        super().__init__(join_type=JoinType.OUTER)


class UserQueryBuilder(Generic[O]):
    def __init__(
        self,
        strategy: JoinStrategy = UserJoinStrategy(),
        join_type: Optional[JoinType] = None,
    ):
        """
        `strategy` по умолчанию инстанс `UserJoinStrategy`
        `join_type` не равный `None` переписывает `JoinType` для стратегии.

        Приоритет:
        join_type (явный) > self._join_type (глобальный) > default_join_type (локальный)
        """
        self._strategy = strategy
        self._join_type = join_type
        self._entities = [UserBase]
        self._joins: list[type[Base]] = []
        self._stmt = select(UserBase)

    def join_admin(self, join_type: Optional[JoinType] = None) -> Self:
        return self.join_model(AdminBase, join_type)

    def join_contractee(self, join_type: Optional[JoinType] = None) -> Self:
        return self.join_model(ContracteeBase, join_type)

    def join_contractor(self, join_type: Optional[JoinType] = None) -> Self:
        return self.join_model(ContractorBase, join_type)

    def join_credentials(self, join_type: Optional[JoinType] = None) -> Self:
        """По умолчанию `JoinType.OUTER`"""
        return self.join_model(WebCredentialsBase, join_type).join_model(
            TelegramCredentialsBase, join_type
        )

    def add_admin(self, join_type: Optional[JoinType] = None) -> Self:
        return self.require_model(AdminBase, join_type)

    def add_contractee(self, join_type: Optional[JoinType] = None) -> Self:
        return self.require_model(ContracteeBase, join_type)

    def add_contractor(self, join_type: Optional[JoinType] = None) -> Self:
        return self.require_model(ContractorBase, join_type)

    def add_credentials(self, join_type: Optional[JoinType] = None) -> Self:
        """По умолчанию `JoinType.OUTER`"""
        return self.require_model(WebCredentialsBase, join_type).require_model(
            TelegramCredentialsBase, join_type
        )

    def require_model(
        self, model: type[Base], join_type: Optional[JoinType] = None
    ) -> Self:
        """Добавляет модель в SELECT и выполняет JOIN, если она ещё не была добавлена ранее."""
        if model not in self._entities:
            self._entities.append(model)
            self._stmt = self._stmt.add_columns(model)
        return self.join_model(model, join_type)

    def join_model(
        self, model: type[Base], join_type: Optional[JoinType] = None
    ) -> Self:
        """Выполняет join модели с указанным типом JOIN, если ещё не был выполнен."""
        if model in self._joins:
            return self

        join_info = self._strategy.get_join(model)
        join_type = join_type or self._join_type or join_info.join_type

        if join_type == JoinType.OUTER:
            self._stmt = self._stmt.outerjoin(
                model, join_info.left == join_info.right
            )
        else:
            self._stmt = self._stmt.join(
                model, join_info.left == join_info.right
            )

        self._joins.append(model)
        return self

    def where_user_id(self, user_id: int) -> Self:
        self._stmt = self._stmt.where(UserBase.user_id == user_id)
        return self

    def apply_contractee_filter(self, filter: ContracteeFilterDTO) -> Self:
        self.join_contractee()
        if filter.gender:
            self._stmt = self._stmt.where(
                ContracteeBase.gender == filter.gender
            )
        if filter.citizenship:
            self._stmt = self._stmt.where(
                ContracteeBase.citizenship == filter.citizenship
            )
        if filter.positions is not None:
            self._stmt = self._stmt.where(
                ContracteeBase.positions == filter.positions
            )
        return self.apply_user_filter(filter)

    def apply_admin_filter(self, filter: AdminFilterDTO) -> Self:
        self.join_admin()
        return self.apply_user_filter(filter)

    def apply_contractor_filter(self, filter: ContractorFilterDTO) -> Self:
        self.join_contractor()
        return self.apply_user_filter(filter)

    def apply_user_filter(self, filter: UserFilterDTO) -> Self:
        if filter.status:
            self._stmt = self._stmt.where(UserBase.status == filter.status)
        if filter.phone_number:
            self._stmt = self._stmt.where(
                UserBase.phone_number == filter.phone_number
            )
        if filter.role:
            self._stmt = self._stmt.where(UserBase.role == filter.role)
        if filter.last_id:
            self._stmt = self._stmt.where(UserBase.user_id > filter.last_id)
        if filter.size:
            self._stmt = self._stmt.limit(filter.size)
        if filter.sorting != SortingOrder.default:
            clause = (
                asc(UserBase.created_at)
                if SortingOrder.ascending
                else desc(UserBase.created_at)
            )
            self._stmt = self._stmt.order_by(clause)
        return self

    # def apply_sorting(self, column: Column, order: SortingOrder) -> Self:
    #     if not self.is_column_joined(column):
    #         raise ValueError(f"No join for column's table: {column.table}")
    #     clause = (
    #         asc(column) if order == SortingOrder.ascending else desc(column)
    #     )
    #     self._stmt = self._stmt.order_by(clause)
    #     return self

    # def is_column_joined(self, column: Column) -> bool:
    #     model = column.table
    #     return model in self._joins

    def build(self) -> Select:
        return self._stmt

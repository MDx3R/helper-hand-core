from sqlalchemy import Row, Select, and_, asc, desc, func, or_, select
from typing import Optional, Self

from domain.dto.base import SortingOrder
from domain.dto.reply.internal.reply_filter_dto import ReplyFilterDTO
from infrastructure.database.models import (
    Base,
    ContracteeBase,
    OrderBase,
    OrderDetailBase,
    ReplyBase,
    UserBase,
)
from infrastructure.repositories.base import (
    JoinInfo,
    JoinStrategy,
    JoinType,
    frozen,
    get_column_value,
)


class ReplyJoinStrategy(JoinStrategy):
    def __init__(self, join_type: JoinType = JoinType.INNER):
        self.join_type = join_type

    def get_strategies(self) -> dict[type[Base], JoinInfo]:
        return {
            OrderDetailBase: JoinInfo(
                ReplyBase.detail_id, OrderDetailBase.detail_id, self.join_type
            ),
            OrderBase: JoinInfo(
                OrderDetailBase.order_id, OrderBase.order_id, self.join_type
            ),
            UserBase: JoinInfo(
                ReplyBase.contractee_id, UserBase.user_id, self.join_type
            ),
            ContracteeBase: JoinInfo(
                ReplyBase.contractee_id,
                ContracteeBase.contractee_id,
                self.join_type,
            ),
        }


ALIASES = {
    "reply": ReplyBase,
    "detail": OrderDetailBase,
    "order": OrderBase,
    "contractee_user": UserBase,
    "contractor": ContracteeBase,
}


@frozen(init=False)
class UnmappedReply:
    _aliases = ALIASES
    reply: ReplyBase
    detail: OrderDetailBase
    order: OrderBase
    contractee_user: UserBase
    contractee: ContracteeBase

    def __init__(self, row: Row):
        for alias, model in self._aliases.items():
            if hasattr(self, alias):
                object.__setattr__(self, alias, get_column_value(row, model))


class ReplyQueryBuilder:
    def __init__(
        self,
        strategy: JoinStrategy = ReplyJoinStrategy(),
        join_type: Optional[JoinType] = None,
    ):
        self._strategy = strategy
        self._join_type = join_type
        self._entities = [ReplyBase]
        self._joins: list[type[Base]] = []
        self._stmt = select(ReplyBase)

    def add_detail(self, join_type: Optional[JoinType] = None) -> Self:
        return self.require_model(OrderDetailBase, join_type)

    def add_order(self, join_type: Optional[JoinType] = None) -> Self:
        self.join_detail(join_type)
        return self.require_model(OrderBase, join_type)

    def add_contractee(self, join_type: Optional[JoinType] = None) -> Self:
        self.require_model(UserBase, join_type)
        return self.require_model(ContracteeBase, join_type)

    def join_order(self, join_type: Optional[JoinType] = None) -> Self:
        self.join_detail(join_type)
        return self.join_model(OrderBase, join_type)

    def join_detail(self, join_type: Optional[JoinType] = None) -> Self:
        return self.join_model(OrderDetailBase, join_type)

    def join_contractee(self, join_type: Optional[JoinType] = None) -> Self:
        self.join_model(UserBase, join_type)
        return self.join_model(ContracteeBase, join_type)

    def require_model(
        self, model: type[Base], join_type: Optional[JoinType] = None
    ) -> Self:
        if model not in self._entities:
            self._entities.append(model)
            self._stmt = self._stmt.add_columns(model)
        return self.join_model(model, join_type)

    def join_model(
        self, model: type[Base], join_type: Optional[JoinType] = None
    ) -> Self:
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

    def where_reply_id(self, contractee_id: int, detail_id: int) -> Self:
        self._stmt = self._stmt.where(
            ReplyBase.contractee_id == contractee_id,
            ReplyBase.detail_id == detail_id,
        )
        return self

    def where_detail_id(self, detail_id: int) -> Self:
        self._stmt = self._stmt.where(ReplyBase.detail_id == detail_id)
        return self

    def where_contractee_id(self, contractee_id: int) -> Self:
        self._stmt = self._stmt.where(ReplyBase.contractee_id == contractee_id)
        return self

    def apply_reply_filter(self, filter: ReplyFilterDTO) -> Self:
        if filter.order_id:
            self.join_detail()
            self._stmt = self._stmt.where(
                OrderDetailBase.order_id == filter.order_id
            )
        if filter.detail_id:
            self.where_detail_id(filter.detail_id)
        if filter.contractee_id:
            self.where_contractee_id(filter.contractee_id)
        if filter.status:
            self._stmt = self._stmt.where(ReplyBase.status == filter.status)
        if filter.dropped:
            self._stmt = self._stmt.where(ReplyBase.dropped == filter.dropped)
        if filter.date:
            self.join_detail()
            self._stmt = self._stmt.where(OrderDetailBase.date == filter.date)
        if filter.starts_after:
            dt = filter.starts_after
            self.join_detail()
            self._stmt = self._stmt.where(
                or_(
                    OrderDetailBase.date > dt.date(),
                    and_(
                        OrderDetailBase.date == dt.date(),
                        OrderDetailBase.start_at > dt.time(),
                    ),
                )
            )
        if filter.starts_before:
            dt = filter.starts_before
            self.join_detail()
            self._stmt = self._stmt.where(
                or_(
                    OrderDetailBase.date < dt.date(),
                    and_(
                        OrderDetailBase.date == dt.date(),
                        OrderDetailBase.start_at < dt.time(),
                    ),
                )
            )
        if filter.last_id:
            self._stmt = self._stmt.where(ReplyBase.reply_id > filter.last_id)
        if filter.size:
            self._stmt = self._stmt.limit(filter.size)
        if filter.sorting != SortingOrder.default:
            clause = (
                asc(ReplyBase.created_at)
                if filter.sorting == SortingOrder.ascending
                else desc(ReplyBase.created_at)
            )
            self._stmt = self._stmt.order_by(clause)
        return self

    def build(self) -> Select:
        return self._stmt

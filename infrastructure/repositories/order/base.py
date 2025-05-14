from datetime import datetime
from sqlalchemy import Alias, Row, Select, and_, asc, desc, func, or_, select
from sqlalchemy.orm import aliased
from sqlalchemy.dialects.postgresql import ARRAY
from typing import Optional, Self

from domain.dto.base import SortingOrder
from domain.dto.order.internal.order_filter_dto import OrderFilterDTO
from domain.entities.order.detail import OrderDetail
from domain.entities.reply.enums import ReplyStatusEnum
from domain.entities.user.admin.admin import Admin
from domain.services.domain.services import (
    OrderDetailDomainService,
    OrderDomainService,
)
from infrastructure.database.models import (
    AdminBase,
    Base,
    ContracteeBase,
    ContractorBase,
    OrderBase,
    OrderDetailBase,
    ReplyBase,
    UserBase,
    WebCredentialsBase,
)
from infrastructure.repositories.base import (
    JoinInfo,
    JoinStrategy,
    JoinType,
    UnmappedEntity,
    frozen,
    get_column_value,
)


class OrderJoinStrategy(JoinStrategy):
    ContractorUserBase = aliased(UserBase)
    AdminUserBase = aliased(UserBase)

    def __init__(self, join_type: JoinType = JoinType.INNER):
        self.join_type = join_type

    def get_strategies(self) -> dict[type[Base], JoinInfo]:
        return {
            OrderDetailBase: JoinInfo(
                OrderBase.order_id, OrderDetailBase.order_id, self.join_type
            ),
            self.ContractorUserBase: JoinInfo(
                OrderBase.contractor_id, UserBase.user_id, self.join_type
            ),
            ContractorBase: JoinInfo(
                OrderBase.contractor_id,
                ContractorBase.contractor_id,
                self.join_type,
            ),
            self.AdminUserBase: JoinInfo(
                OrderBase.admin_id, UserBase.user_id, self.join_type
            ),
            AdminBase: JoinInfo(
                OrderBase.admin_id, AdminBase.admin_id, self.join_type
            ),
            ReplyBase: JoinInfo(
                OrderDetailBase.detail_id,
                ReplyBase.detail_id,
                self.join_type,
            ),
        }


ALIASES = {
    "order": OrderBase,
    "detail": OrderDetailBase,
    "admin_user": OrderJoinStrategy.AdminUserBase,
    "admin": AdminBase,
    "contractor_user": OrderJoinStrategy.ContractorUserBase,
    "contractor": ContractorBase,
}


@frozen(init=False)
class UnmappedOrder(UnmappedEntity):
    _aliases = ALIASES
    order: OrderBase
    detail: OrderDetailBase
    contractor_user: UserBase
    contractor: ContractorBase
    admin_user: Optional[UserBase]
    admin: Optional[AdminBase]


class OrderQueryBuilder:
    def __init__(
        self,
        strategy: JoinStrategy = OrderJoinStrategy(),
        join_type: Optional[JoinType] = None,
    ):
        self._strategy = strategy
        self._join_type = join_type
        self._entities = [OrderBase]
        self._joins: list[type[Base]] = []
        self._stmt = select(OrderBase)

    def add_detail(self, join_type: Optional[JoinType] = None) -> Self:
        return self.require_model(OrderDetailBase, join_type)

    def add_contractor(self, join_type: Optional[JoinType] = None) -> Self:
        self.require_model(OrderJoinStrategy.ContractorUserBase, join_type)
        return self.require_model(ContractorBase, join_type)

    def add_admin(self, join_type: Optional[JoinType] = None) -> Self:
        self.require_model(OrderJoinStrategy.ContractorUserBase, join_type)
        return self.require_model(AdminBase, join_type)

    def join_detail(self, join_type: Optional[JoinType] = None) -> Self:
        return self.join_model(OrderDetailBase, join_type)

    def join_contractor(self, join_type: Optional[JoinType] = None) -> Self:
        self.join_model(OrderJoinStrategy.ContractorUserBase, join_type)
        return self.join_model(ContractorBase, join_type)

    def join_admin(self, join_type: Optional[JoinType] = None) -> Self:
        self.join_model(OrderJoinStrategy.AdminUserBase, join_type)
        return self.join_model(AdminBase, join_type)

    def join_reply(self, join_type: Optional[JoinType] = None) -> Self:
        self.join_detail(join_type)
        return self.join_model(ReplyBase, join_type)

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

    def where_order_id(self, order_id: int) -> Self:
        self._stmt = self._stmt.where(OrderBase.order_id == order_id)
        return self

    def where_detail_id(self, detail_id: int) -> Self:
        self.join_detail()
        self._stmt = self._stmt.where(OrderDetailBase.detail_id == detail_id)
        return self

    def apply_order_filter(self, filter: OrderFilterDTO) -> Self:
        if filter.order_id:
            self._stmt = self._stmt.where(
                OrderBase.order_id == filter.order_id
            )
        if filter.status:
            self._stmt = self._stmt.where(OrderBase.status == filter.status)
        if filter.contractor_id:
            self._stmt = self._stmt.where(
                OrderBase.contractor_id == filter.contractor_id
            )
        if filter.admin_id:
            self._stmt = self._stmt.where(
                OrderBase.admin_id == filter.admin_id
            )
        if filter.contractee_id:
            self.join_reply()
            self._stmt = self._stmt.where(
                ReplyBase.contractee_id == filter.contractee_id
            )
        if filter.only_available_details:
            self.apply_only_available_details()
        if filter.last_id:
            self._stmt = self._stmt.where(OrderBase.order_id > filter.last_id)
        if filter.size:
            self._stmt = self._stmt.limit(filter.size)
        if filter.sorting != SortingOrder.default:
            clause = (
                asc(OrderBase.created_at)
                if filter.sorting == SortingOrder.ascending
                else desc(OrderBase.created_at)
            )
            self._stmt = self._stmt.order_by(clause)
        return self

    def apply_only_available_details(self) -> Self:
        self.join_detail()
        min_datetime = datetime.now() + OrderDetailDomainService.starts_after
        self._stmt = self._stmt.where(
            or_(
                OrderDetailBase.date > min_datetime.date(),
                and_(
                    OrderDetailBase.date == min_datetime.date(),
                    OrderDetailBase.start_at > min_datetime.time(),
                ),
            )
        )

        subquery = (
            select(func.count())
            .select_from(ReplyBase)
            .where(
                ReplyBase.detail_id == OrderDetail.detail_id,
                ReplyBase.status == ReplyStatusEnum.accepted,
                ReplyBase.dropped == False,
            )
            .scalar_subquery()
        )

        self._stmt = self._stmt.where(OrderDetailBase.count > subquery)
        return self

    def build(self) -> Select:
        return self._stmt

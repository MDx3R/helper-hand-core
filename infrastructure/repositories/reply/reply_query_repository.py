from typing import List

from sqlalchemy import func, select

from domain.dto.reply.internal.base import ReplyIdDTO
from domain.dto.reply.internal.reply_filter_dto import (
    CountRepliesDTO,
    ReplyFilterDTO,
)
from domain.entities.reply.available_replies_for_detail import (
    AvailableRepliesForDetail,
)
from domain.entities.reply.reply import Reply
from domain.repositories.reply.reply_query_repository import (
    ReplyQueryRepository,
)
from infrastructure.database.mappers import ReplyMapper
from infrastructure.database.models import (
    OrderBase,
    OrderDetailBase,
    ReplyBase,
)
from infrastructure.repositories.base import QueryExecutor
from infrastructure.repositories.reply.base import ReplyQueryBuilder


class ReplyQueryRepositoryImpl(ReplyQueryRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def get_reply(self, query: ReplyIdDTO) -> Reply | None:
        stmt = (
            self._get_query_builder()
            .where_reply_id(query.contractee_id, query.detail_id)
            .build()
        )

        reply = await self.executor.execute_scalar_one(stmt)
        if not reply:
            return None
        return ReplyMapper.to_model(reply)

    async def filter_replies(self, query: ReplyFilterDTO) -> List[Reply]:
        stmt = self._get_query_builder().apply_reply_filter(query).build()

        replies = await self.executor.execute_scalar_many(stmt)
        return [ReplyMapper.to_model(reply) for reply in replies]

    async def get_detail_available_replies_count(
        self, detail_id: int
    ) -> AvailableRepliesForDetail:
        stmt = (
            select(
                OrderDetailBase.detail_id,
                (OrderDetailBase.count - func.count(ReplyBase.reply_id)).label(
                    "quantity"
                ),
            )
            .outerjoin(
                ReplyBase, ReplyBase.detail_id == OrderDetailBase.detail_id
            )
            .where(OrderDetailBase.detail_id == detail_id)
            .group_by(OrderDetailBase.detail_id, OrderDetailBase.count)
        )

        result = await self.executor.execute_one(stmt)
        if result is None:
            return AvailableRepliesForDetail(detail_id=detail_id, quantity=0)

        return AvailableRepliesForDetail(
            detail_id=result.detail_id, quantity=result.quantity
        )

    async def get_order_available_replies_count(
        self, order_id: int
    ) -> List[AvailableRepliesForDetail]:
        stmt = (
            select(
                OrderDetailBase.detail_id,
                (OrderDetailBase.count - func.count(ReplyBase.reply_id)).label(
                    "quantity"
                ),
            )
            .join(OrderBase, OrderBase.order_id == OrderDetailBase.order_id)
            .outerjoin(
                ReplyBase, ReplyBase.detail_id == OrderDetailBase.detail_id
            )
            .where(OrderBase.order_id == order_id)
            .group_by(OrderDetailBase.detail_id, OrderDetailBase.count)
        )

        result = await self.executor.execute_many(stmt)

        return [
            AvailableRepliesForDetail(
                detail_id=i.detail_id, quantity=i.quantity
            )
            for i in result
        ]

    def _get_query_builder(self) -> ReplyQueryBuilder:
        return ReplyQueryBuilder()

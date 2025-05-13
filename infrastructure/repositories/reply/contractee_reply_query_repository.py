from datetime import date
from typing import List

from domain.dto.base import SortingOrder
from domain.dto.order.internal.order_query_dto import GetUserOrderDTO
from domain.dto.reply.internal.reply_filter_dto import (
    ContracteeReplyFilterDTO,
    ReplyFilterDTO,
)
from domain.entities.reply.reply import Reply
from domain.entities.user.contractee.contractee import Contractee
from domain.repositories.reply.contractee_reply_query_repository import (
    ContracteeReplyQueryRepository,
)
from domain.services.domain.services import OrderDetailDomainService
from infrastructure.database.mappers import ReplyMapper
from infrastructure.repositories.base import QueryExecutor
from infrastructure.repositories.reply.base import ReplyQueryBuilder


class ContracteeReplyQueryRepositoryImpl(ContracteeReplyQueryRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def get_contractee_future_replies(self, user_id: int) -> List[Reply]:
        stmt = (
            self._get_query_builder()
            .apply_reply_filter(
                ReplyFilterDTO(
                    contractee_id=user_id,
                    starts_after=OrderDetailDomainService.get_min_start_time(),
                    sorting=SortingOrder.descending,
                )
            )
            .build()
            .limit(None)  # Сбрасываем, так как устанавливается по умолчанию 15
        )

        replies = await self.executor.execute_scalar_many(stmt)
        return ReplyMapper.to_model_list(replies)

    async def get_contractee_order_replies(
        self, query: GetUserOrderDTO
    ) -> List[Reply]:
        stmt = (
            self._get_query_builder()
            .apply_reply_filter(
                ReplyFilterDTO(
                    contractee_id=query.user_id,
                    order_id=query.order_id,
                )
            )
            .build()
        )

        replies = await self.executor.execute_scalar_many(stmt)
        return ReplyMapper.to_model_list(replies)

    async def contractee_has_reply(
        self, query: ContracteeReplyFilterDTO
    ) -> bool:
        stmt = (
            self._get_query_builder()
            .apply_contractee_reply_filter(query)
            .build()
        )
        return bool(await self.executor.execute_scalar_one(stmt))

    def _get_query_builder(self) -> ReplyQueryBuilder:
        return ReplyQueryBuilder()

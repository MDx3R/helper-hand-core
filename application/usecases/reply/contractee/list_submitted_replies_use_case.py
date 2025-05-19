from typing import List
from application.usecases.reply.reply_query_use_case import (
    ListOrderRepliesUseCase,
)
from domain.dto.base import SortingOrder
from domain.dto.reply.internal.reply_filter_dto import ReplyFilterDTO
from domain.dto.reply.internal.reply_query_dto import GetOrderRepliesDTO
from domain.dto.reply.response.reply_output_dto import ReplyOutputDTO
from domain.dto.user.internal.user_context_dto import PaginatedDTO
from domain.mappers.reply_mappers import ReplyMapper
from domain.repositories.reply.reply_query_repository import (
    ReplyQueryRepository,
)


class ListSubmittedRepliesUseCase:
    def __init__(self, repository: ReplyQueryRepository):
        self.repository = repository

    async def execute(self, query: PaginatedDTO) -> List[ReplyOutputDTO]:
        replies = await self.repository.filter_replies(
            ReplyFilterDTO(
                contractee_id=query.context.user_id,
                last_id=query.last_id,
                size=query.size,
                sorting=SortingOrder.descending,
            )
        )
        return [ReplyMapper.to_output(i) for i in replies]


class ListSubmittedRepliesForOrderUseCase(ListOrderRepliesUseCase):
    def __init__(self, repository: ReplyQueryRepository):
        super().__init__(repository)

    def _build_filter(self, query: GetOrderRepliesDTO) -> ReplyFilterDTO:
        return ReplyFilterDTO(
            contractee_id=query.context.user_id,
            order_id=query.order_id,
            last_id=query.last_id,
            size=query.size,
            sorting=SortingOrder.descending,
        )

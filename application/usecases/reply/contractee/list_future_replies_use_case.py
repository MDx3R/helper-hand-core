from typing import List
from domain.dto.base import SortingOrder
from domain.dto.reply.internal.reply_filter_dto import ReplyFilterDTO
from domain.dto.reply.response.reply_output_dto import CompleteReplyOutputDTO
from domain.dto.user.internal.user_context_dto import PaginatedDTO
from domain.mappers.reply_mappers import ReplyMapper
from domain.repositories.reply.composite_reply_query_repository import (
    CompositeReplyQueryRepository,
)
from domain.services.domain.services import OrderDetailDomainService


class ListFutureRepliesForContracteeUseCase:
    def __init__(self, repository: CompositeReplyQueryRepository):
        self.repository = repository

    async def execute(
        self, query: PaginatedDTO
    ) -> List[CompleteReplyOutputDTO]:
        replies = await self.repository.filter_complete_replies(
            ReplyFilterDTO(
                contractee_id=query.context.user_id,
                starts_after=OrderDetailDomainService.get_min_start_time(),
                sorting=SortingOrder.descending,
            )
        )
        return [ReplyMapper.to_complete(i) for i in replies]

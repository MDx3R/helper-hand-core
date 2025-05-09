from typing import List
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
        replies = self.repository.filter_replies(
            ReplyFilterDTO(
                contractee_id=query.context.user_id,
                last_id=query.last_id,
                size=query.size,
                sorting="descending",
            )
        )
        return [ReplyMapper.to_output(i) for i in replies]


class ListSubmittedRepliesForOrderUseCase:
    def __init__(self, repository: ReplyQueryRepository):
        self.repository = repository

    async def execute(self, query: GetOrderRepliesDTO) -> List[ReplyOutputDTO]:
        replies = self.repository.filter_replies(
            ReplyFilterDTO(
                contractee_id=query.context.user_id,
                last_id=query.last_id,
                size=query.size,
                sorting="descending",
            )
        )
        return [ReplyMapper.to_output(i) for i in replies]

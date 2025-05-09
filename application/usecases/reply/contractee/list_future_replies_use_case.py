from typing import List
from domain.dto.reply.response.reply_output_dto import ReplyOutputDTO
from domain.dto.user.internal.base import UserIdDTO
from domain.dto.user.internal.user_context_dto import PaginatedDTO
from domain.mappers.reply_mappers import ReplyMapper
from domain.repositories.reply.contractee_reply_query_repository import (
    ContracteeReplyQueryRepository,
)


class ListFutureRepliesUseCase:
    def __init__(self, repository: ContracteeReplyQueryRepository):
        self.repository = repository

    async def execute(self, query: PaginatedDTO) -> List[ReplyOutputDTO]:
        replies = self.repository.get_contractee_future_replies(
            UserIdDTO(user_id=query.context.user_id)
        )
        return [ReplyMapper.to_output(i) for i in replies]

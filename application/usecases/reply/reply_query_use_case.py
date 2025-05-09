from typing import List
from domain.dto.reply.internal.reply_filter_dto import ReplyFilterDTO
from domain.dto.reply.internal.reply_query_dto import (
    GetContracteeRepliesDTO,
    GetDetailRepliesDTO,
    GetOrderRepliesDTO,
    GetReplyDTO,
)
from domain.dto.reply.response.reply_output_dto import (
    CompleteReplyOutputDTO,
    ReplyOutputDTO,
)
from domain.mappers.reply_mappers import ReplyMapper
from domain.repositories.reply.composite_reply_query_repository import (
    CompositeReplyQueryRepository,
)
from domain.repositories.reply.contractee_reply_query_repository import (
    ContracteeReplyQueryRepository,
)
from domain.repositories.reply.reply_query_repository import (
    ReplyQueryRepository,
)


# Common
class GetReplyUseCase:
    def __init__(self, repository: CompositeReplyQueryRepository):
        self.repository = repository

    async def execute(
        self, query: GetReplyDTO
    ) -> CompleteReplyOutputDTO | None:
        reply = self.repository.get_complete_reply(query)
        if not reply:
            return None
        return ReplyMapper.to_complete(reply)


# Order's
class ListOrderRepliesUseCase:
    def __init__(self, repository: ReplyQueryRepository):
        self.repository = repository

    async def execute(self, query: GetOrderRepliesDTO) -> List[ReplyOutputDTO]:
        replies = self.repository.filter_replies(
            ReplyFilterDTO(
                order_id=query.order_id,
                last_id=query.last_id,
                size=query.size,
            )
        )
        return [ReplyMapper.to_output(i) for i in replies]


class ListDetailRepliesUseCase:
    def __init__(self, repository: ReplyQueryRepository):
        self.repository = repository

    async def execute(
        self, query: GetDetailRepliesDTO
    ) -> List[ReplyOutputDTO]:
        replies = self.repository.filter_replies(
            ReplyFilterDTO(
                detail_id=query.detail_id,
                last_id=query.last_id,
                size=query.size,
            )
        )

        return [ReplyMapper.to_output(i) for i in replies]


# Contractee's
class ListContracteeRepliesUseCase:
    def __init__(self, repository: ReplyQueryRepository):
        self.repository = repository

    async def execute(
        self, query: GetContracteeRepliesDTO
    ) -> List[ReplyOutputDTO]:
        replies = self.repository.filter_replies(
            ReplyFilterDTO(
                contractee_id=query.user_id,
                last_id=query.last_id,
                size=query.size,
                sorting="descending",
            )
        )
        return [ReplyMapper.to_output(i) for i in replies]


class ListContracteeFutureRepliesUseCase:
    def __init__(self, repository: ContracteeReplyQueryRepository):
        self.repository = repository

    async def execute(
        self, query: GetContracteeRepliesDTO
    ) -> List[ReplyOutputDTO]:
        replies = self.repository.get_contractee_future_replies(query)
        return [ReplyMapper.to_output(i) for i in replies]

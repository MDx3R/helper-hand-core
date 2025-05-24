from typing import List
from domain.dto.base import SortingOrder
from domain.dto.reply.internal.reply_filter_dto import ReplyFilterDTO
from domain.dto.reply.internal.reply_query_dto import (
    GetContracteeRepliesDTO,
    GetDetailRepliesDTO,
    GetOrderRepliesDTO,
    GetReplyDTO,
)
from domain.dto.reply.response.reply_output_dto import CompleteReplyOutputDTO
from domain.mappers.reply_mappers import ReplyMapper
from domain.repositories.reply.composite_reply_query_repository import (
    CompositeReplyQueryRepository,
)


# Common
class GetReplyUseCase:
    def __init__(self, reply_repository: CompositeReplyQueryRepository):
        self.reply_repository = reply_repository

    async def execute(
        self, query: GetReplyDTO
    ) -> CompleteReplyOutputDTO | None:
        reply = await self.reply_repository.get_complete_reply(query)
        if not reply:
            return None
        return ReplyMapper.to_complete(reply)


# Order's
class ListOrderRepliesUseCase:
    def __init__(self, repository: CompositeReplyQueryRepository):
        self.repository = repository

    async def execute(
        self, query: GetOrderRepliesDTO
    ) -> List[CompleteReplyOutputDTO]:
        replies = await self.repository.filter_complete_replies(
            self._build_filter(query)
        )
        return [ReplyMapper.to_complete(i) for i in replies]

    def _build_filter(self, query: GetOrderRepliesDTO) -> ReplyFilterDTO:
        return ReplyFilterDTO(
            order_id=query.order_id,
            last_id=query.last_id,
            size=query.size,
            sorting=SortingOrder.descending,
        )


class ListDetailRepliesUseCase:
    def __init__(self, repository: CompositeReplyQueryRepository):
        self.repository = repository

    # TODO: Изменить возвращаемый тип
    async def execute(
        self, query: GetDetailRepliesDTO
    ) -> List[CompleteReplyOutputDTO]:
        replies = await self.repository.filter_complete_replies(
            ReplyFilterDTO(
                detail_id=query.detail_id,
                last_id=query.last_id,
                size=query.size,
            )
        )

        return [ReplyMapper.to_complete(i) for i in replies]


# Contractee's
class ListContracteeRepliesUseCase:
    def __init__(self, repository: CompositeReplyQueryRepository):
        self.repository = repository

    # TODO: Изменить возвращаемый тип
    async def execute(
        self, query: GetContracteeRepliesDTO
    ) -> List[CompleteReplyOutputDTO]:
        replies = await self.repository.filter_complete_replies(
            ReplyFilterDTO(
                contractee_id=query.user_id,
                last_id=query.last_id,
                size=query.size,
                sorting=SortingOrder.descending,
            )
        )
        return [ReplyMapper.to_complete(i) for i in replies]

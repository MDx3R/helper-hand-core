from typing import List
from application.usecases.reply.reply_query_use_case import (
    ListOrderRepliesUseCase,
)
from domain.dto.reply.internal.reply_filter_dto import ReplyFilterDTO
from domain.dto.reply.internal.reply_query_dto import (
    GetDetailRepliesDTO,
    GetOrderRepliesDTO,
)
from domain.dto.reply.response.reply_output_dto import CompleteReplyOutputDTO
from domain.mappers.reply_mappers import ReplyMapper
from domain.repositories.reply.composite_reply_query_repository import (
    CompositeReplyQueryRepository,
)


class ListOrderRepliesForContractorUseCase(ListOrderRepliesUseCase):
    async def execute(
        self, query: GetOrderRepliesDTO
    ) -> List[CompleteReplyOutputDTO]:
        # TODO: Проверка на заказ и заказчика
        return await super().execute(query)


class ListDetailRepliesForContractorUseCase:
    def __init__(self, repository: CompositeReplyQueryRepository):
        self.repository = repository

    async def execute(
        self, query: GetDetailRepliesDTO
    ) -> List[CompleteReplyOutputDTO]:
        # TODO: Проверка на заказ и заказчика
        replies = await self.repository.filter_complete_replies(
            ReplyFilterDTO(
                detail_id=query.detail_id,
                last_id=query.last_id,
                size=query.size,
            )
        )

        return [ReplyMapper.to_complete(i) for i in replies]

from typing import List
from domain.dto.reply.internal.reply_filter_dto import ReplyFilterDTO
from domain.dto.reply.internal.reply_query_dto import (
    GetDetailRepliesDTO,
    GetOrderRepliesDTO,
)
from domain.dto.reply.response.reply_output_dto import ReplyOutputDTO
from domain.mappers.reply_mappers import ReplyMapper
from domain.repositories.reply.reply_query_repository import (
    ReplyQueryRepository,
)


class ListOrderRepliesForContractorUseCase:
    def __init__(self, repository: ReplyQueryRepository):
        self.repository = repository

    async def execute(self, query: GetOrderRepliesDTO) -> List[ReplyOutputDTO]:
        # TODO: Проверка на заказ и заказчика
        replies = self.repository.filter_replies(
            ReplyFilterDTO(
                order_id=query.order_id,
                last_id=query.last_id,
                size=query.size,
            )
        )
        return [ReplyMapper.to_output(i) for i in replies]


class ListDetailRepliesForContractorUseCase:
    def __init__(self, repository: ReplyQueryRepository):
        self.repository = repository

    async def execute(
        self, query: GetDetailRepliesDTO
    ) -> List[ReplyOutputDTO]:
        # TODO: Проверка на заказ и заказчика
        replies = self.repository.filter_replies(
            ReplyFilterDTO(
                detail_id=query.detail_id,
                last_id=query.last_id,
                size=query.size,
            )
        )

        return [ReplyMapper.to_output(i) for i in replies]

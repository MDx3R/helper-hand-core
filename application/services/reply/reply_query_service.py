from typing import List
from application.usecases.reply.reply_query_use_case import (
    GetReplyUseCase,
    ListOrderRepliesUseCase,
)
from domain.dto.reply.internal.reply_query_dto import (
    GetOrderRepliesDTO,
    GetReplyDTO,
)
from domain.dto.reply.response.reply_output_dto import (
    CompleteReplyOutputDTO,
    ReplyOutputDTO,
)


class BaseReplyService:
    def __init__(
        self,
        get_reply_use_case: GetReplyUseCase,
        get_order_replies_use_case: ListOrderRepliesUseCase,
    ):
        self.get_reply_use_case = get_reply_use_case
        self.get_order_replies_use_case = get_order_replies_use_case

    async def get_reply(
        self, query: GetReplyDTO
    ) -> CompleteReplyOutputDTO | None:
        return await self.get_reply_use_case.execute(query)

    async def get_order_replies(
        self, query: GetOrderRepliesDTO
    ) -> List[CompleteReplyOutputDTO]:
        return await self.get_order_replies_use_case.execute(query)

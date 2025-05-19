from abc import ABC, abstractmethod
from typing import List

from domain.dto.reply.internal.reply_query_dto import (
    GetOrderRepliesDTO,
    GetReplyDTO,
)
from domain.dto.reply.request.create_reply_dto import CreateReplyDTO
from domain.dto.reply.response.reply_output_dto import (
    CompleteReplyOutputDTO,
    ReplyOutputDTO,
)
from domain.dto.user.internal.user_context_dto import PaginatedDTO
from domain.entities.reply.composite_reply import CompleteReply


class ContracteeReplyManagmentService(ABC):
    @abstractmethod
    async def submit_reply(self, request: CreateReplyDTO) -> ReplyOutputDTO:
        pass


class ContracteeReplyQueryService(ABC):
    @abstractmethod
    async def get_reply(
        self, query: GetReplyDTO
    ) -> CompleteReplyOutputDTO | None:
        pass

    @abstractmethod
    async def get_replies(self, query: PaginatedDTO) -> List[ReplyOutputDTO]:
        pass

    @abstractmethod
    async def get_order_replies(
        self, query: GetOrderRepliesDTO
    ) -> List[ReplyOutputDTO]:
        pass

    @abstractmethod
    async def get_future_replies(
        self, query: PaginatedDTO
    ) -> List[ReplyOutputDTO]:
        pass

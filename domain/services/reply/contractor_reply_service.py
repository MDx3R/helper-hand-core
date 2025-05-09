from abc import ABC, abstractmethod
from typing import List

from domain.dto.reply.internal.reply_managment_dto import (
    ApproveReplyDTO,
    DisapproveReplyDTO,
)
from domain.dto.reply.internal.reply_query_dto import (
    GetDetailRepliesDTO,
    GetOrderRepliesDTO,
    GetOrderReplyDTO,
    GetReplyDTO,
)
from domain.dto.reply.response.reply_output_dto import (
    CompleteReplyOutputDTO,
    ReplyOutputDTO,
)


class ContractorReplyManagmentService(ABC):
    @abstractmethod
    async def approve_reply(self, request: ApproveReplyDTO) -> ReplyOutputDTO:
        pass

    @abstractmethod
    async def disapprove_reply(
        self, request: DisapproveReplyDTO
    ) -> ReplyOutputDTO:
        pass


class ContractorReplyService(ABC):
    @abstractmethod
    async def get_reply(
        self, query: GetReplyDTO
    ) -> CompleteReplyOutputDTO | None:
        pass

    @abstractmethod
    async def get_pending_reply(
        self, query: GetOrderReplyDTO
    ) -> CompleteReplyOutputDTO | None:
        pass

    @abstractmethod
    async def get_order_replies(
        self, query: GetOrderRepliesDTO
    ) -> List[ReplyOutputDTO]:
        pass

    @abstractmethod
    async def get_detail_replies(
        self, query: GetDetailRepliesDTO
    ) -> List[ReplyOutputDTO]:
        pass

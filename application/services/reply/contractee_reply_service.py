from typing import List
from application.external.notification.notification_service import (
    ContractorReplyNotificationService,
)
from application.usecases.reply.contractee.create_reply_use_case import (
    CreateReplyUseCase,
)
from application.usecases.reply.contractee.get_reply_use_case import (
    GetReplyForContracteeUseCase,
)
from application.usecases.reply.contractee.list_submitted_replies_use_case import (
    ListSubmittedRepliesForOrderUseCase,
    ListSubmittedRepliesUseCase,
)
from application.usecases.reply.reply_query_use_case import (
    GetReplyUseCase,
    ListContracteeFutureRepliesUseCase,
)
from domain.dto.reply.internal.reply_query_dto import (
    GetContracteeRepliesDTO,
    GetOrderRepliesDTO,
    GetReplyDTO,
)
from domain.dto.reply.request.create_reply_dto import CreateReplyDTO
from domain.dto.reply.response.reply_output_dto import ReplyOutputDTO
from domain.dto.user.internal.user_context_dto import PaginatedDTO
from domain.entities.reply.composite_reply import CompleteReply
from domain.services.reply.contractee_reply_service import (
    ContracteeReplyManagmentService,
    ContracteeReplyService,
)


class ContracteeReplyManagmentServiceImpl(ContracteeReplyManagmentService):
    def __init__(
        self,
        create_reply_use_case: CreateReplyUseCase,
        contractor_notification_service: ContractorReplyNotificationService,
    ):
        self.create_reply_use_case = create_reply_use_case
        self.contractor_notification_service = contractor_notification_service

    async def submit_reply(self, request: CreateReplyDTO) -> ReplyOutputDTO:
        reply = await self.create_reply_use_case.execute(request)
        await self.contractor_notification_service.send_new_reply_notification()  # TODO: DTO
        return reply


class ContracteeReplyServiceImpl(ContracteeReplyService):
    def __init__(
        self,
        get_reply_use_case: GetReplyForContracteeUseCase,
        get_replies_use_case: ListSubmittedRepliesUseCase,
        get_order_replies_use_case: ListSubmittedRepliesForOrderUseCase,
        get_future_replies_use_case: ListContracteeFutureRepliesUseCase,
    ):
        self.get_reply_use_case = get_reply_use_case
        self.get_replies_use_case = get_replies_use_case
        self.get_order_replies_use_case = get_order_replies_use_case
        self.get_future_replies_use_case = get_future_replies_use_case

    async def get_reply(self, query: GetReplyDTO) -> CompleteReply | None:
        return await self.get_reply_use_case.execute(query)

    async def get_replies(self, query: PaginatedDTO) -> List[ReplyOutputDTO]:
        return await self.get_replies_use_case.execute(query)

    async def get_order_replies(
        self, query: GetOrderRepliesDTO
    ) -> List[ReplyOutputDTO]:
        return await self.get_order_replies_use_case.execute(query)

    async def get_future_replies(
        self, query: GetContracteeRepliesDTO
    ) -> List[ReplyOutputDTO]:
        return await self.get_future_replies_use_case.execute(query)

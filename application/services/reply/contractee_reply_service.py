from typing import List
from application.external.notification.notification_service import (
    ContractorReplyNotificationService,
)
from application.usecases.reply.create_reply_use_case import CreateReplyUseCase
from application.usecases.reply.reply_query_use_case import (
    GetCompleteReplyUseCase,
    ListContracteeFutureRepliesUseCase,
)
from domain.dto.reply.internal.reply_query_dto import (
    GetContracteeRepliesDTO,
    GetReplyDTO,
)
from domain.dto.reply.request.create_reply_dto import CreateReplyDTO
from domain.dto.reply.response.reply_output_dto import ReplyOutputDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO
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
        get_reply_use_case: GetCompleteReplyUseCase,
        get_future_replies_use_case: ListContracteeFutureRepliesUseCase,
    ):
        self.get_reply_use_case = get_reply_use_case
        self.get_future_replies_use_case = get_future_replies_use_case

    async def get_reply(self, query: GetReplyDTO) -> CompleteReply | None:
        return await self.get_reply_use_case.execute(query)

    async def get_future_replies(
        self, query: GetContracteeRepliesDTO
    ) -> List[ReplyOutputDTO]:
        return await self.get_future_replies_use_case.execute(query)

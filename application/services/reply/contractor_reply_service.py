from application.external.notification.notification_service import (
    ContracteeReplyNotificationService,
)
from application.usecases.reply.change_reply_status_use_case import (
    ApproveReplyUseCase,
    DisapproveReplyUseCase,
)
from application.usecases.reply.contractor.reply_query_use_case import (
    GetCompleteReplyForContractorUseCase,
    GetPendingReplyUseCase,
)
from domain.dto.reply.internal.reply_managment_dto import (
    ApproveReplyDTO,
    DisapproveReplyDTO,
)
from domain.dto.reply.internal.reply_query_dto import (
    GetOrderReplyDTO,
    GetReplyDTO,
)
from domain.dto.reply.response.reply_output_dto import (
    CompleteReplyOutputDTO,
    ReplyOutputDTO,
)
from domain.services.reply.contractor_reply_service import (
    ContractorReplyManagmentService,
    ContractorReplyService,
)


class ContractorReplyManagmentServiceImpl(ContractorReplyManagmentService):
    def __init__(
        self,
        approve_reply_use_case: ApproveReplyUseCase,
        disapprove_reply_use_case: DisapproveReplyUseCase,
        contractee_notification_service: ContracteeReplyNotificationService,
    ):
        self.approve_reply_use_case = approve_reply_use_case
        self.disapprove_reply_use_case = disapprove_reply_use_case
        self.contractee_notification_service = contractee_notification_service

    async def approve_reply(self, request: ApproveReplyDTO) -> ReplyOutputDTO:
        reply = await self.approve_reply_use_case.execute(request)
        await self.contractee_notification_service.send_reply_approved_notification()  # TODO: DTO
        return reply

    async def disapprove_reply(
        self, request: DisapproveReplyDTO
    ) -> ReplyOutputDTO:
        reply = await self.disapprove_reply_use_case.execute(request)
        await self.contractee_notification_service.send_reply_disapproved_notification()  # TODO: DTO
        return reply


class ContractorReplyServiceImpl(ContractorReplyService):
    def __init__(
        self,
        get_reply_use_case: GetCompleteReplyForContractorUseCase,
        get_pending_reply_use_case: GetPendingReplyUseCase,
    ):
        self.get_reply_use_case = get_reply_use_case
        self.get_pending_reply_use_case = get_pending_reply_use_case

    async def get_reply(
        self, query: GetReplyDTO
    ) -> CompleteReplyOutputDTO | None:
        return await self.get_reply_use_case.execute(query)

    async def get_pending_reply(
        self, query: GetOrderReplyDTO
    ) -> CompleteReplyOutputDTO | None:
        return await self.get_pending_reply_use_case.execute(query)

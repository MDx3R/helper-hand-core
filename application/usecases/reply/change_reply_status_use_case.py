from typing import List, Tuple
from application.transactions import transactional
from domain.dto.order.internal.base import OrderIdDTO
from domain.dto.order.internal.user_command_dto import SetOrderStatusDTO
from domain.dto.reply.internal.base import ReplyIdDTO
from domain.dto.reply.internal.reply_command_dto import SetReplyStatusDTO
from domain.dto.reply.internal.reply_filter_dto import ContracteeReplyFilterDTO
from domain.dto.reply.internal.reply_managment_dto import (
    ApproveReplyDTO,
    DisapproveReplyDTO,
    DropRepliesDTO,
    ReplyManagementDTO,
)
from domain.dto.reply.response.reply_output_dto import ReplyOutputDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.entities.order.detail import OrderDetail
from domain.entities.order.enums import OrderStatusEnum
from domain.entities.order.order import Order
from domain.entities.reply.available_replies_for_detail import (
    AvailableRepliesForDetail,
)
from domain.entities.reply.composite_reply import CompleteReply
from domain.entities.reply.enums import ReplyStatusEnum
from domain.entities.reply.reply import Reply
from domain.exceptions.service.auth import UnauthorizedAccessException
from domain.exceptions.service.common import NotFoundException
from domain.exceptions.service.orders import OrderActionNotAllowedException
from domain.exceptions.service.replies import (
    DetailFullException,
    ReplyStatusChangeNotAllowedException,
)
from domain.mappers.reply_mappers import ReplyMapper
from domain.repositories.order.order_command_repository import (
    OrderCommandRepository,
)
from domain.repositories.reply.composite_reply_query_repository import (
    CompositeReplyQueryRepository,
)
from domain.repositories.reply.reply_command_repository import (
    ReplyCommandRepository,
)
from domain.repositories.reply.reply_query_repository import (
    ReplyQueryRepository,
)
from domain.services.domain.services import (
    AvailabilityDomainService,
    OrderDomainService,
    ReplyDomainService,
)


class ApproveReplyUseCase:
    def __init__(
        self,
        reply_query_repository: ReplyQueryRepository,
        reply_command_repository: ReplyCommandRepository,
        composite_query_repository: CompositeReplyQueryRepository,
        order_repository: OrderCommandRepository,
    ):
        self.reply_query_repository = reply_query_repository
        self.reply_command_repository = reply_command_repository
        self.composite_query_repository = composite_query_repository
        self.order_repository = order_repository

    @transactional
    async def execute(self, request: ApproveReplyDTO) -> ReplyOutputDTO:
        # Отклик
        composite_reply = (
            await self._get_complete_reply_and_raise_if_not_exists(request)
        )
        # Проверка на доступность
        self._check_contractor_access(composite_reply, request.context)
        self._check_reply_can_be_approved(composite_reply)

        detail_availability, order_availability = (
            await self._get_order_and_detail_availability(composite_reply)
        )

        # Исключение, возникающие, когда все места на заказ заняты, не имеет смысла,
        # так как позиция на заказ не может быть доступной в случае недоступности заказа.
        if AvailabilityDomainService.is_full(detail_availability):
            raise DetailFullException()

        reply = await self._change_reply_status(
            composite_reply.reply, ReplyStatusEnum.accepted
        )
        # обновляем количество свободных мест на позицию
        detail_availability.quantity -= 1

        await self._drop_unapproved_replies_by_date(
            reply.contractee_id, composite_reply.detail.date
        )

        await self._update_order_and_drop_replies_if_full(
            composite_reply, detail_availability, order_availability
        )

        return ReplyMapper.to_output(reply)

    async def _change_reply_status(
        self, reply: Reply, status: ReplyStatusEnum
    ) -> Reply:
        return await self.reply_command_repository.set_reply_status(
            SetReplyStatusDTO(
                contractee_id=reply.contractee_id,
                detail_id=reply.detail_id,
                status=status,
            )
        )

    async def _drop_unapproved_replies_by_date(
        self, composite_reply: CompleteReply
    ):
        await self.reply_command_repository.drop_replies(
            ContracteeReplyFilterDTO(
                contractee_id=composite_reply.reply.contractee_id,
                date=composite_reply.detail.date,
            )
        )

    async def _update_order_and_drop_replies_if_full(
        self,
        reply: CompleteReply,
        detail_availability: AvailableRepliesForDetail,
        order_availability: List[AvailableRepliesForDetail],
    ):
        if AvailabilityDomainService.are_all_full(order_availability):
            await self._close_order_and_drop_unapproved_replies(reply.order)
        elif AvailabilityDomainService.is_full(detail_availability):
            await self._drop_unapproved_replies_for_detail(reply.detail)

    async def _drop_unapproved_replies_for_detail(self, detail: OrderDetail):
        await self.reply_command_repository.drop_replies(
            ContracteeReplyFilterDTO(
                detail_id=detail.detail_id,
            )
        )

    async def _close_order_and_drop_unapproved_replies(self, order: Order):
        await self.order_repository.set_order_status(
            SetOrderStatusDTO(
                order_id=order.order_id, status=OrderStatusEnum.closed
            )
        )
        await self.reply_command_repository.drop_replies(
            ContracteeReplyFilterDTO(
                order_id=order.order_id,
            )
        )

    async def _get_complete_reply_and_raise_if_not_exists(
        self, request: ReplyManagementDTO
    ) -> CompleteReply:
        reply = await self.composite_query_repository.get_complete_reply(
            ReplyIdDTO(
                contractee_id=request.contractee_id,
                detail_id=request.detail_id,
            )
        )
        if not reply:
            raise NotFoundException(
                f"{request.contractee_id, request.detail_id}"
            )

        return reply

    def _check_contractor_access(
        self, reply: CompleteReply, context: UserContextDTO
    ):
        if not OrderDomainService.is_owned_by(reply.order, context.user_id):
            raise UnauthorizedAccessException()

    def _check_reply_can_be_approved(self, composite_reply: CompleteReply):
        order = composite_reply.order
        if not OrderDomainService.can_have_replies(order):
            raise OrderActionNotAllowedException(
                order.order_id, order.status, "Подтверждение отклика"
            )
        reply = composite_reply.reply
        if not ReplyDomainService.can_be_approved(reply):
            raise ReplyStatusChangeNotAllowedException(
                reply.contractee_id,
                reply.detail_id,
                reply.status,
                "Подтверждение отклика",
            )

    async def _get_order_and_detail_availability(
        self, reply: CompleteReply
    ) -> Tuple[AvailableRepliesForDetail, List[AvailableRepliesForDetail]]:
        order_availability = await self._get_order_availability(
            reply.order.order_id
        )
        detail_availability = await self._get_detail_availability(
            reply.detail.detail_id, order_availability
        )

        return detail_availability, order_availability

    async def _check_if_detail_is_full(
        self, detail_availability: AvailableRepliesForDetail
    ):
        # Исключение, возникающие, когда все места на заказ заняты, не имеет смысла,
        # так как позиция на заказ не может быть доступной в случае недоступности заказа.
        if AvailabilityDomainService.is_full(detail_availability):
            raise DetailFullException()

    async def _get_order_availability(
        self, order_id: int
    ) -> List[AvailableRepliesForDetail]:
        return await self.reply_query_repository.get_order_available_replies_count(
            OrderIdDTO(order_id=order_id)
        )

    async def _get_detail_availability(
        self,
        detail_id: int,
        order_availability: List[AvailableRepliesForDetail],
    ) -> AvailableRepliesForDetail:
        for detail_availability in order_availability:
            if detail_availability.detail_id == detail_id:
                return detail_availability

        raise ValueError  # Не может быть поднята


class DisapproveReplyUseCase:
    def __init__(
        self,
        reply_command_repository: ReplyCommandRepository,
        composite_query_repository: CompositeReplyQueryRepository,
    ):
        self.reply_command_repository = reply_command_repository
        self.composite_query_repository = composite_query_repository

    @transactional
    async def execute(self, request: DisapproveReplyDTO) -> ReplyOutputDTO:
        # Отклик
        composite_reply = (
            await self._get_complete_reply_and_raise_if_not_exists(request)
        )
        # Проверка на доступность
        self._check_contractor_access(composite_reply, request.context)
        self._check_reply_can_be_approved(composite_reply)

        reply = await self._change_reply_status(
            composite_reply.reply, ReplyStatusEnum.disapproved
        )

        return ReplyMapper.to_output(reply)

    async def _change_reply_status(
        self, reply: Reply, status: ReplyStatusEnum
    ) -> Reply:
        return await self.reply_command_repository.set_reply_status(
            SetReplyStatusDTO(
                contractee_id=reply.contractee_id,
                detail_id=reply.detail_id,
                status=status,
            )
        )

    async def _get_complete_reply_and_raise_if_not_exists(
        self, request: ReplyManagementDTO
    ) -> CompleteReply:
        reply = await self.composite_query_repository.get_complete_reply(
            ReplyIdDTO(
                contractee_id=request.contractee_id,
                detail_id=request.detail_id,
            )
        )

        if not reply:
            raise NotFoundException(
                f"{request.contractee_id, request.detail_id}"
            )

        return reply

    def _check_contractor_access(
        self, reply: CompleteReply, context: UserContextDTO
    ):
        if not OrderDomainService.is_owned_by(reply.order, context.user_id):
            raise UnauthorizedAccessException()

    def _check_reply_can_be_approved(self, composite_reply: CompleteReply):
        order = composite_reply.order
        if not OrderDomainService.can_have_replies(order):
            raise OrderActionNotAllowedException(
                order.order_id, order.status, "Подтверждение отклика"
            )
        reply = composite_reply.reply
        if not ReplyDomainService.can_be_approved(reply):
            raise ReplyStatusChangeNotAllowedException(
                reply.contractee_id,
                reply.detail_id,
                reply.status,
                "Подтверждение отклика",
            )


# NOTE: Может не использоваться
class DropRepliesUseCase:
    """Использовать исключительно для системных задач"""

    def __init__(
        self,
        repository: ReplyCommandRepository,
    ):
        self.repository = repository

    @transactional
    async def execute(self, request: DropRepliesDTO) -> List[ReplyOutputDTO]:
        replies = await self.repository.drop_replies(
            ContracteeReplyFilterDTO(
                order_id=request.order_id,
                detail_id=request.detail_id,
                contractee_id=request.contractee_id,
            )
        )
        return [ReplyMapper.to_output(i) for i in replies]

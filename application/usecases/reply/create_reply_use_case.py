from datetime import date
from typing import Tuple
from application.transactions.transactional import transactional
from domain.dto.order.internal.base import DetailIdDTO
from domain.dto.reply.internal.reply_filter_dto import ContracteeReplyFilterDTO
from domain.dto.reply.request.create_reply_dto import CreateReplyDTO
from domain.dto.reply.response.reply_output_dto import ReplyOutputDTO
from domain.dto.user.internal.base import UserIdDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.entities.order.detail import OrderDetail
from domain.entities.order.order import Order
from domain.entities.reply.enums import ReplyStatusEnum
from domain.entities.reply.reply import Reply
from domain.entities.user.contractee.contractee import Contractee
from domain.exceptions.service.common import NotFoundException
from domain.exceptions.service.replies import ReplySubmitNotAllowedException
from domain.mappers.reply_mappers import ReplyMapper
from domain.repositories.order.detail.order_detail_query_repository import (
    OrderDetailQueryRepository,
)
from domain.repositories.order.order_query_repository import (
    OrderQueryRepository,
)
from domain.repositories.reply.contractee_reply_query_repository import (
    ContracteeReplyQueryRepository,
)
from domain.repositories.reply.reply_command_repository import (
    ReplyCommandRepository,
)
from domain.repositories.reply.reply_query_repository import (
    ReplyQueryRepository,
)
from domain.repositories.user.contractee.contractee_query_repository import (
    ContracteeQueryRepository,
)
from domain.services.domain.services import (
    AvailabilityDomainService,
    OrderDetailDomainService,
    OrderDomainService,
)
from domain.wager import calculate_pay


class CreateReplyUseCase:
    def __init__(
        self,
        contractee_repository: ContracteeQueryRepository,
        order_repository: OrderQueryRepository,
        detail_repository: OrderDetailQueryRepository,
        reply_query_repository: ReplyQueryRepository,
        reply_command_repository: ReplyCommandRepository,
        contractee_reply_repository: ContracteeReplyQueryRepository,
    ):
        self.contractee_repository = contractee_repository
        self.order_repository = order_repository
        self.detail_repository = detail_repository
        self.reply_query_repository = reply_query_repository
        self.reply_command_repository = reply_command_repository
        self.contractee_reply_repository = contractee_reply_repository

    @transactional
    async def execute(self, request: CreateReplyDTO) -> ReplyOutputDTO:
        # Исполнитель
        contractee = await self._get_contractee_and_raise_if_not_exists(
            request.context
        )
        # Проверка заказа
        order, detail = (
            await self._get_order_and_detail_and_raise_if_not_exists(
                request.detail_id
            )
        )
        # Проверка доступа
        await self._check_reply_can_be_submitted(order, detail, contractee)

        # Сохранение отклика
        reply = await self._save_reply(request, detail, contractee)
        return ReplyMapper.to_output(reply)

    async def _save_reply(
        self,
        request: CreateReplyDTO,
        detail: OrderDetail,
        contractee: Contractee,
    ) -> Reply:
        wager = calculate_pay(detail.wager)

        reply = await self.reply_command_repository.create_reply(
            ReplyMapper.from_create(request, contractee.user_id, wager)
        )
        return reply

    async def _get_contractee_and_raise_if_not_exists(
        self, context: UserContextDTO
    ) -> Contractee:
        contractee = self.contractee_repository.get_contractee(
            UserIdDTO(user_id=context.user_id)
        )

        if not contractee:
            raise NotFoundException(context.user_id)

    async def _get_order_and_detail_and_raise_if_not_exists(
        self, detail_id: int
    ) -> Tuple[Order, OrderDetail]:
        dto = DetailIdDTO(detail_id=detail_id)
        detail = await self.detail_repository.get_detail(dto)
        if not detail:
            raise NotFoundException(detail_id)

        # нет необходимости проверять заказ на существование,
        # так как проверка detail уже обеспечила его существование
        order = await self.order_repository.get_order_for_detail(dto)

        return order, detail

    async def _check_reply_can_be_submitted(
        self, order: Order, detail: OrderDetail, contractee: Contractee
    ):
        if not OrderDomainService.can_have_replies(order):
            raise ReplySubmitNotAllowedException("Заказ не является открытым")

        if not OrderDetailDomainService.is_suitable(detail, contractee):
            raise ReplySubmitNotAllowedException(
                "Отклик на позицию недопустим для конкретного исполнителя"
            )

        if not OrderDetailDomainService.is_relevant_at_current_time(detail):
            raise ReplySubmitNotAllowedException(
                "Позиция больше не является допустимой для отклика"
            )

        if await self._is_contractee_busy_on_date(contractee, detail.date):
            raise ReplySubmitNotAllowedException(
                "Отклик на выбранную дату недопустим"
            )

        if await self._has_contractee_replied_to_detail(contractee, detail):
            raise ReplySubmitNotAllowedException(
                "Уже имеется отклик на выбранную позицию"
            )

        if await self._is_detail_full(detail):
            raise ReplySubmitNotAllowedException(
                "На выбранную позицию не осталось свободных мест"
            )

    async def _is_contractee_busy_on_date(
        self, contractee: Contractee, date: date
    ) -> bool:
        return await self.contractee_reply_repository.contractee_has_reply(
            ContracteeReplyFilterDTO(
                contractee_id=contractee.contractee_id,
                status=ReplyStatusEnum.accepted,
                date=date,
            )
        )

    async def _has_contractee_replied_to_detail(
        self, contractee: Contractee, detail: OrderDetail
    ) -> bool:
        return await self.contractee_reply_repository.contractee_has_reply(
            ContracteeReplyFilterDTO(
                contractee_id=contractee.contractee_id,
                detail_id=detail.detail_id,
            )
        )

    async def _is_detail_full(self, detail: OrderDetail) -> bool:
        detail_availability = await self.reply_query_repository.get_detail_available_replies_count(
            DetailIdDTO(detail_id=detail.detail_id)
        )
        return AvailabilityDomainService.is_full(detail_availability)

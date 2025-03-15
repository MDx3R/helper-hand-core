from typing import List, Tuple

from datetime import datetime

from domain.models import Contractee, Order, DetailedOrder, OrderDetail, Reply
from domain.wager import calculate_wager
from domain.models.enums import OrderStatusEnum
from domain.services.reply import ContracteeReplyService
from domain.repositories import ReplyRepository, OrderRepository, OrderDetailRepository, UserRepository
from domain.exceptions.service import NotFoundException, ReplySubmitNotAllowedException

from application.external.notification import ContractorNotificationService
from application.transactions import TransactionManager, transactional
from application.dtos.input import ReplyInputDTO
from application.dtos.output import ReplyOutputDTO, DetailedReplyOutputDTO

from domain.services.domain import OrderDomainService, OrderDetailDomainService, AvailabilityDomainService

class ContracteeReplyServiceImpl(ContracteeReplyService):
    """
    Класс реализации интерфейса `ContracteeReplyService` для управления откликами исполнителя.
    
    Attributes:
        order_repository (OrderRepository): Репозиторий с данными заказов.
        order_detail_repository (OrderDetailRepository): Репозиторий с данными сведений заказов.
        reply_repository (ReplyRepository): Репозиторий с данными откликов.
        transaction_manager (TransactionManager): Менеджер транзакций.
        contractor_notification_service (ContractorNotificationService): Сервис уведомлений заказчика.
    """

    def __init__(self, 
                 order_repository: OrderRepository,
                 order_detail_repository: OrderDetailRepository,
                 reply_repository: ReplyRepository,
                 transaction_manager: TransactionManager,
                 contractor_notification_service: ContractorNotificationService
    ):
        self.order_repository = order_repository
        self.order_detail_repository = order_detail_repository
        self.reply_repository = reply_repository
        self.transaction_manager = transaction_manager
        self.contractor_notification_service = contractor_notification_service

    async def submit_reply_to_order(self, reply_input: ReplyInputDTO, contractee: Contractee) -> ReplyOutputDTO:
        async with self.transaction_manager:

            order, detail = await self._get_order_and_detail_and_check_access(reply_input.detail_id)

            await self._check_reply_can_be_submitted(order, detail, contractee)

            reply = await self._save_reply(detail, contractee)

        await self._notify_contractor_on_new_reply(order, detail, contractee)

        return ReplyOutputDTO.from_reply(reply)

    async def _save_reply(self, detail: OrderDetail, contractee: Contractee) -> Reply:
        wager = calculate_wager(detail.wager)
        reply = await self.reply_repository.save_reply(
            Reply(
                contractee_id=contractee.contractee_id,
                detail_id=detail.detail_id,
                wager=wager
            )
        )
        return reply

    async def _get_order_and_detail_and_check_access(self, detail_id: int) -> Tuple[Order, OrderDetail]:
        detail = await self.order_detail_repository.get_detail_by_id(detail_id)
        if detail is None: 
            raise NotFoundException(detail_id)
        
        # нет необходимости проверять заказ на существование, 
        # так как проверка detail уже обеспечила его существование
        order = await self.order_repository.get_order_by_detail_id(detail_id)

        return order, detail

    async def _check_reply_can_be_submitted(self, order: Order, detail: OrderDetail, contractee: Contractee):
        if not OrderDomainService.can_have_replies(order):
            raise ReplySubmitNotAllowedException("Заказ не является открытым")
        
        if not OrderDetailDomainService.is_suitable(detail, contractee):
            raise ReplySubmitNotAllowedException("Отклик на позицию недопустим для конкретного исполнителя")

        if not OrderDetailDomainService.is_relevant_at_current_time(detail):
            raise ReplySubmitNotAllowedException("Позиция больше не является допустимой для отклика")
        
        if await self._is_contractee_busy_on_date(contractee, detail.date):
            raise ReplySubmitNotAllowedException("Отклик на выбранную дату недопустим")

        if await self._has_contractee_replied_to_detail(contractee, detail):
            raise ReplySubmitNotAllowedException("Уже имеется отклик на выбранную позицию")

        if await self._is_detail_full(detail):
            raise ReplySubmitNotAllowedException("На выбранную позицию не осталось свободных мест")

    async def _is_contractee_busy_on_date(self, contractee: Contractee, date: datetime) -> bool:
        return await self.reply_repository.is_contractee_busy_on_date(contractee.contractee_id, date)

    async def _has_contractee_replied_to_detail(self, contractee: Contractee, detail: OrderDetail) -> bool:
        return await self.reply_repository.has_contractee_replied_to_detail(detail.detail_id, contractee.contractee_id)

    async def _is_detail_full(self, detail: OrderDetail) -> bool:
        detail_availability = await self.reply_repository.get_available_replies_count_by_detail_id(detail.detail_id)
        return AvailabilityDomainService.is_full(detail_availability)

    async def _notify_contractor_on_new_reply(self, order: Order, detail: OrderDetail, contractee: Contractee):
        contractor = await self.order_repository.get_contractor_by_order_id(detail.order_id)
        await self.contractor_notification_service.send_new_reply_notification(contractor)

    async def get_reply(self, contractee_id: int, detail_id: int, contractee: Contractee) -> DetailedReplyOutputDTO | None:
        if contractee_id != contractee.contractee_id:
            return None
        
        reply = await self.reply_repository.get_detailed_reply(contractee_id, detail_id)
        if not reply:
            return None
        
        return DetailedReplyOutputDTO.from_reply(reply)

    async def get_replies(self, contractee: Contractee, page: int = 1, size: int = 10) -> List[DetailedReplyOutputDTO]:
        replies = await self.reply_repository.get_detailed_replies_by_contractee_id_by_page(contractee.contractee_id, page, size)
        return [DetailedReplyOutputDTO.from_reply(reply) for reply in replies]

    async def get_approved_replies(self, contractee: Contractee, page: int = 1, size: int = 10) -> List[DetailedReplyOutputDTO]:
        replies = await self.reply_repository.get_approved_detailed_replies_by_contractee_id_by_page(contractee.contractee_id, page, size)
        return [DetailedReplyOutputDTO.from_reply(reply) for reply in replies]

    async def get_unapproved_replies(self, contractee: Contractee, page: int = 1, size: int = 10) -> List[DetailedReplyOutputDTO]:
        replies = await self.reply_repository.get_unapproved_detailed_replies_by_contractee_id_by_page(contractee.contractee_id, page, size)
        return [DetailedReplyOutputDTO.from_reply(reply) for reply in replies]
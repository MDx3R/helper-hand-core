from typing import List

from domain.models import Contractee
from domain.wager import calculate_wager
from domain.models.enums import OrderStatusEnum
from domain.services.reply import ContracteeReplyService
from domain.repositories import ReplyRepository, OrderRepository, OrderDetailRepository, UserRepository
from domain.exceptions.service import NotFoundException, ReplySubmitNotAllowedException
from domain.time import is_current_time_valid_for_reply

from application.external.notification import ContractorNotificationService
from application.transactions import TransactionManager, transactional
from application.dtos.input import ReplyInputDTO
from application.dtos.output import ReplyOutputDTO, DetailedReplyOutputDTO

class ContracteeReplyServiceImpl(ContracteeReplyService):
    """
    Класс реализации интерфейса `ContracteeReplyService` для управления откликами исполнителя.
    
    Attributes:
        user_repository (UserRepository): Репозиторий с данными пользователей.
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
        """
        Реализация метода `submit_reply_to_order` из `ContracteeReplyService`.
        """
        # объявляем транзакцию
        async with self.transaction_manager:

            detail = await self.order_detail_repository.get_detail_by_id(reply_input.detail_id)
            if detail is None: 
                raise NotFoundException(reply_input.detail_id)
            
            order = await self.order_repository.get_order_by_detail_id(reply_input.detail_id)
            # нет необходимости проверять заказ на существование, 
            # так как проверка detail уже обеспечила его существование
            if order.status != OrderStatusEnum.open:
                raise ReplySubmitNotAllowedException("Заказ не является открытым")
            
            if detail.gender and detail.gender != contractee.gender:
                raise ReplySubmitNotAllowedException("Отклик на позицию недопустим для конкретного исполнителя")

            if not is_current_time_valid_for_reply(detail.start_date): # нужно ли?
                raise ReplySubmitNotAllowedException("Позиция больше не является допустимой для отклика")
            
            if await self.reply_repository.is_contractee_busy_on_date(detail.date):
                raise ReplySubmitNotAllowedException("Отклик на выбранную дату недопустим")

            if await self.reply_repository.has_contractee_replied_to_detail(detail.detail_id, contractee.contractee_id):
                raise ReplySubmitNotAllowedException("Уже имеется отклик на выбранную позицию")

            detail_availability = await self.reply_repository.get_available_replies_count_by_detail_id(detail.detail_id)
            if detail_availability.is_full():
                raise ReplySubmitNotAllowedException("На выбранную позицию не осталось свободных мест")

            wager = calculate_wager(detail.wager)

            reply = await self.reply_repository.save_reply(reply_input.to_reply(wager))

        contractor = await self.order_repository.get_contractor_by_order_id(detail.order_id)
        await self.contractor_notification_service.send_new_reply_notification(contractor)

        return ReplyOutputDTO.from_reply(reply)

    async def get_replies(self, contractee: Contractee) -> List[DetailedReplyOutputDTO]:
        """
        Реализация метода `get_replies` из `ContracteeReplyService`.
        """
        replies = await self.reply_repository.get_replies_by_contractee_id(contractee.contractee_id)
        return [DetailedReplyOutputDTO.from_reply(reply) for reply in replies]

    async def get_approved_replies(self, contractee: Contractee) -> List[DetailedReplyOutputDTO]:
        """
        Реализация метода `get_approved_replies` из `ContracteeReplyService`.
        """
        replies = await self.reply_repository.get_approved_replies_by_contractee_id(contractee.contractee_id)
        return [DetailedReplyOutputDTO.from_reply(reply) for reply in replies]

    async def get_unapproved_replies(self, contractee: Contractee) -> List[DetailedReplyOutputDTO]:
        """
        Реализация метода `get_unapproved_replies` из `ContracteeReplyService`.
        """
        replies = await self.reply_repository.get_unapproved_replies_by_contractee_id(contractee.contractee_id)
        return [DetailedReplyOutputDTO.from_reply(reply) for reply in replies]
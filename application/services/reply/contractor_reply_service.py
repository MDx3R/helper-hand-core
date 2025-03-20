from typing import List, Tuple

from datetime import date

from domain.entities import Contractor, Reply, DetailedReply, Order, OrderDetail, AvailableRepliesForDetail, Contractee
from domain.entities.enums import ReplyStatusEnum, OrderStatusEnum

from domain.services.reply import ContractorReplyService
from domain.repositories import ReplyRepository, OrderRepository, OrderDetailRepository, UserRepository
from application.external.notification import ContracteeNotificationService, ContractorNotificationService, AdminNotificationService
from domain.dto.output import ReplyOutputDTO, DetailedReplyOutputDTO
from application.transactions import TransactionManager, transactional
from domain.exceptions.service import (
    UnauthorizedAccessException, 
    NotFoundException, 
    DetailFullException, 
    OrderActionNotAllowedException,
    ReplyStatusChangeNotAllowedException
)
from domain.services.domain import OrderDomainService, ReplyDomainService, AvailabilityDomainService

class ContractorReplyServiceImpl(ContractorReplyService):
    """
    Класс реализации интерфейса `ContractorReplyService` для управления откликами заказчика.
    
    Attributes:
        user_repository (UserRepository): Репозиторий с данными пользователей.
        order_repository (OrderRepository): Репозиторий с данными заказов.
        order_detail_repository (OrderDetailRepository): Репозиторий с данными сведений заказов.
        reply_repository (ReplyRepository): Репозиторий с данными откликов.
        transaction_manager (TransactionManager): Менеджер транзакций.
        contractee_notification_service (ContracteeNotificationService): Сервис уведомлений исполнителей.
    """

    def __init__(
        self, 
        user_repository: UserRepository,
        order_repository: OrderRepository,
        order_detail_repository: OrderDetailRepository,
        reply_repository: ReplyRepository, 
        transaction_manager: TransactionManager,
        admin_notification_service : AdminNotificationService,
        contractor_notification_service: ContractorNotificationService,
        contractee_notification_service: ContracteeNotificationService
    ):
        self.user_repository = user_repository
        self.order_repository = order_repository
        self.order_detail_repository = order_detail_repository
        self.reply_repository = reply_repository
        self.transaction_manager = transaction_manager
        self.admin_notification_service = admin_notification_service
        self.contractor_notification_service = contractor_notification_service
        self.contractee_notification_service = contractee_notification_service

    async def get_first_unapproved_reply(self, contractor: Contractor) -> DetailedReplyOutputDTO | None:
        reply = await self.reply_repository.get_first_unapproved_reply_by_contractor_id(contractor.contractor_id)
        if reply is None:
            return None

        return DetailedReplyOutputDTO.from_reply(reply)

    async def get_first_unapproved_reply_for_order(self, order_id: int, contractor: Contractor) -> DetailedReplyOutputDTO | None:
        reply = await self.reply_repository.get_first_unapproved_reply_by_order_id_and_contractor_id(order_id, contractor.contractor_id)
        if reply is None:
            return None

        return DetailedReplyOutputDTO.from_reply(reply)

    async def get_unapproved_replies_for_order(self, order_id: int, contractor: Contractor, page: int = 1, size: int = 20) -> List[DetailedReplyOutputDTO]:
        replies = await self.reply_repository.get_unapproved_replies_by_order_id_and_contractor_id_by_page(order_id, contractor.contractor_id, page, size)

        return [DetailedReplyOutputDTO.from_reply(rep) for rep in replies]

    async def get_approved_replies_for_order(self, order_id: int, contractor: Contractor, page: int = 1, size: int = 20) -> List[DetailedReplyOutputDTO]:
        replies = await self.reply_repository.get_approved_replies_by_order_id_and_contractor_id_by_page(order_id, contractor.contractor_id, page, size)

        return [DetailedReplyOutputDTO.from_reply(rep) for rep in replies]

    async def approve_reply(self, contractee_id: int, detail_id: int, contractor: Contractor) -> DetailedReplyOutputDTO:
        # объявляем транзакцию
        async with self.transaction_manager:
            detailed_reply = await self._get_detailed_reply_and_check_access(contractee_id, detail_id, contractor)
            order, detail = detailed_reply.order, detailed_reply.detail

            await self._check_reply_can_be_approved(order, detailed_reply)
            detail_availability, order_availability = await self._get_order_and_detail_availability_and_check_if_full(detail)
            
            detailed_reply = await self._change_detailed_reply_status(detailed_reply, ReplyStatusEnum.accepted)
            detail_availability.quantity -= 1 # обновляем количество свободных мест на позицию (todo: проверить, будет ли обновлено для order_availability)

            await self._drop_unapproved_replies_by_date(detailed_reply.contractee_id, detail.date)

            order, dropped_contractees = await self._update_order_and_replies_if_full(order, detail, detail_availability, order_availability)
            detailed_reply.order = order # явно присваиваем объект заказа

        await self._send_notifications_on_reply_approval(contractor, detailed_reply, dropped_contractees)

        return DetailedReplyOutputDTO.from_reply(detailed_reply)

    async def disapprove_reply(self, contractee_id: int, detail_id: int, contractor: Contractor) -> DetailedReplyOutputDTO:
        # объявляем транзакцию
        async with self.transaction_manager:
            detailed_reply = await self._get_detailed_reply_and_check_access(contractee_id, detail_id, contractor)

            await self._check_reply_can_be_approved(detailed_reply.order, detailed_reply)

            detailed_reply = await self._change_detailed_reply_status(detailed_reply, ReplyStatusEnum.dropped)

        await self._notify_disapproved_contractee(detailed_reply)

        return DetailedReplyOutputDTO.from_reply(detailed_reply)
    
    async def _get_detailed_reply_and_check_access(self, contractee_id: int, detail_id: int, contractor: Contractor) -> DetailedReply:
        """
        Получает отклик на заказ, а также проверяет может ли заказчик изменять заказ.
        """
        reply = await self.reply_repository.get_detailed_reply(contractee_id, detail_id)
        
        if reply is None:
            raise NotFoundException()
        
        if not OrderDomainService.is_owned_by(reply.order, contractor.contractor_id):
            raise UnauthorizedAccessException()
        
        return reply
    
    async def _change_detailed_reply_status(self, reply: DetailedReply, status: ReplyStatusEnum) -> DetailedReply:
        await self.reply_repository.change_reply_status(reply.contractee_id, reply.detail_id, status)
        reply.status = status
        return reply

    async def _check_reply_can_be_approved(order: Order, reply: Reply):
        """
        Проверяет:
        - Возможность изменения статуса отклика по статусу заказа (подтвердить или отклонить отклик можно только для заказов со статусом `OrderStatusEnum.open`)
        - Является ли статус отклика отличным от `ReplyStatusEnum.created`. Иные статусы не могут быть изменены на подтвержденный.

        Raises:
            OrderActionNotAllowedException: Возникает, если невозможно поменять статус отклика из-за статуса заказа.
            ReplyStatusChangeNotAllowedException: Возникает, если невозможно поменять статус отклика из-за его исходного статуса.
        """
        if not OrderDomainService.can_have_replies(order):
            raise OrderActionNotAllowedException(order.order_id, order.status, "Подтверждение отклика")

        if not ReplyDomainService.can_be_approved(reply):
            raise ReplyStatusChangeNotAllowedException(reply.contractee_id, reply.detail_id, reply.status, "Подтверждение отклика")

    async def _get_order_and_detail_availability_and_check_if_full(self, order: Order, detail: OrderDetail) -> Tuple[AvailableRepliesForDetail, List[AvailableRepliesForDetail]]:
        """
        Получает и проверяет доступность заказа и конкретной позиции.

        Raises:
            DetailFullException: Возникает, если все места на позицию заняты.

        Исключение, возникающие, когда все места на заказ заняты, не имеет смысла, так как позиция на заказ не может быть доступной в случае недоступности заказа.
        """
        order_availability = await self._get_order_availability(order.order_id)
        detail_availability = await self._get_detail_availability(detail.detail_id, order_availability)

        if AvailabilityDomainService.is_full(detail_availability):
            raise DetailFullException()

        return detail_availability, order_availability
       
    async def _get_order_availability(self, order_id: int) -> List[AvailableRepliesForDetail]:
        return await self.reply_repository.get_available_replies_count_for_details_by_order_id(order_id)
    
    async def _get_detail_availability(self, detail_id: int, order_availability: List[AvailableRepliesForDetail]) -> AvailableRepliesForDetail:
        for detail_availability in order_availability:
            if detail_availability.detail_id == detail_id:
                return detail_availability

    async def _close_order_and_drop_unapproved_replies(self, order: Order) -> Tuple[Order, List[DetailedReply]]:
        order = await self.order_repository.change_order_status(order.order_id, OrderStatusEnum.closed)
        dropped_contractees = await self.reply_repository.drop_unapproved_order_replies_by_order_id(order.order_id)

        return order, dropped_contractees

    async def _drop_unapproved_replies_for_detail(self, detail: OrderDetail):
        return await self.reply_repository.drop_unapproved_order_detail_replies_by_detail_id(detail.detail_id)

    async def _update_order_and_replies_if_full(self, order: Order, detail: OrderDetail, detail_availability: AvailableRepliesForDetail, order_availability: List[AvailableRepliesForDetail]) -> Tuple[Order, List[DetailedReply]]:
        """
        Обновляет заказ и отклики, если на заказ или позицию не осталось мест.

        Объект `order` будет отличатся от переданного только в том случае, если его на заказ не осталось свободных мест - заказ будет закрыт.
        Список `dropped_contractees` будет иметь элементы, только если на заказ или позицию не осталось мест и были неподтвержденные отклики.

        Returns:
            Tuple[Order, List[DetailedReply]]: Пара из заказа и списка отмененных откликов. Список отмененных откликов может быть пустым
        """
        
        if AvailabilityDomainService.are_all_full(order_availability):
            return await self._close_order_and_drop_unapproved_replies(order)
        elif AvailabilityDomainService.is_full(detail_availability):
            dropped_contractees = await self._drop_unapproved_replies_for_detail(detail)
            return order, dropped_contractees

        return order, []

    async def _send_notifications_on_reply_approval(self, contractor: Contractor, detailed_reply: DetailedReply, dropped_contractees: List[Contractee]):
        """
        Отправляет уведомления, связанные с подтверждением отклика:
        - подтверждённому исполнителю;
        - отменённым исполнителям (если есть);
        - заказчику и администратору, если заказ закрыт.
        """
        order = detailed_reply.order

        if dropped_contractees:
            await self._notify_dropped_contractees(dropped_contractees, order, detailed_reply.detail)

        if OrderDomainService.is_closed(order):
            await self._notify_contractor_and_admin_on_order_closed(contractor, order)

        # отправляется позже всего, чтобы первым сообщением в ленте было уведомление о подтверждении, 
        # так как dropped_contractees может содержать другие отзывы исполнителя на тот же заказ
        await self._notify_approved_contractee(detailed_reply)

    async def _notify_approved_contractee(self, detailed_reply: DetailedReply):
        await self.contractee_notification_service.send_reply_approved_notification(detailed_reply.contractee, detailed_reply.order, detailed_reply.detail)

    async def _notify_disapproved_contractee(self, detailed_reply: DetailedReply):
        await self.contractee_notification_service.send_reply_disapproved_notification(detailed_reply.contractee, detailed_reply.order, detailed_reply.detail)

    async def _notify_dropped_contractees(self, dropped_contractees: List[Contractee], order: Order, detail: OrderDetail):
        if OrderDomainService.is_closed(order):
            await self.contractee_notification_service.send_order_full_notification_many(dropped_contractees, order)
        else:
            await self.contractee_notification_service.send_order_detail_full_notification_many(dropped_contractees, order, detail)

    async def _notify_contractor_and_admin_on_order_closed(self, contractor: Contractor, order: Order):
        await self.contractor_notification_service.send_order_closed_automatically_notification(contractor, order)
        
        admin = await self.user_repository.get_admin_by_id(order.admin_id)
        await self.admin_notification_service.send_order_closed_automatically_notification(admin, order)

    async def _drop_unapproved_replies_by_date(self, contractee_id: int, date: date):
        await self.reply_repository.drop_contractee_unapproved_replies_by_date(contractee_id, date)
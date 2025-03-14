from typing import List, Tuple

from domain.models import Contractor, Order, OrderDetail, DetailedOrder, Contractee
from domain.models.enums import OrderStatusEnum

from domain.services.order import ContractorOrderService
from domain.repositories import (
    UserRepository,
    OrderRepository, 
    ReplyRepository, 
    OrderDetailRepository
)
from application.external.notification import (
    AdminNotificationService, 
    ContracteeNotificationService
)
from application.transactions import TransactionManager, transactional
from application.dtos.input import OrderInputDTO, OrderDetailInputDTO
from application.dtos.output import DetailedOrderOutputDTO, OrderOutputDTO, DetailedReplyOutputDTO
from domain.exceptions.service import (
    MissingOrderDetailsException, 
    OrderStatusChangeNotAllowedException, 
    UnauthorizedAccessException, 
    NotFoundException
)
from domain.services.domain import OrderDomainService

class ContractorOrderServiceImpl(ContractorOrderService):
    """
    Класс реализации интерфейса `ContractorOrderService` для управления заказами заказчика.

    Attributes:
        user_repository (UserRepository): Репозиторий с данными пользователей.
        order_repository (OrderRepository): Репозиторий с данными заказов.
        order_detail_repository (OrderDetailRepository): Репозиторий с данными сведений заказов.
        reply_repository (ReplyRepository): Репозиторий с данными откликов.
        transaction_manager (TransactionManager): Менеджер транзакций.
        admin_notification_service (AdminNotificationService): Сервис уведомлений для администраторов.
        contractee_notification_service (ContracteeNotificationService): Сервис уведомлений для исполнителей.
    """

    def __init__(
        self, 
        user_repository: UserRepository,
        order_repository: OrderRepository, 
        order_detail_repository: OrderDetailRepository,
        reply_repository: ReplyRepository,
        transaction_manager: TransactionManager,
        admin_notification_service: AdminNotificationService, 
        contractee_notification_service: ContracteeNotificationService
    ):
        self.user_repository = user_repository
        self.order_repository = order_repository
        self.order_detail_repository = order_detail_repository
        self.reply_repository = reply_repository
        self.transaction_manager = transaction_manager
        self.admin_notification_service = admin_notification_service
        self.contractee_notification_service = contractee_notification_service

    async def create_order(self, order_input: OrderInputDTO, details_input: List[OrderDetailInputDTO], contractor: Contractor) -> DetailedOrderOutputDTO:
        self._check_order_input_is_complete(order_input, details_input)
        
        # объявляем транзакцию
        async with self.transaction_manager:
            order, details = await self._save_order_and_details(order_input, details_input, contractor)

        await self._notify_admins_on_new_order(order, details)

        return DetailedOrderOutputDTO.from_order_and_details(order, details)

    def _check_order_input_is_complete(self, order: OrderInputDTO, details: List[OrderDetailInputDTO]):
        if len(details) == 0:
            raise MissingOrderDetailsException("Отсутствуют сведения заказа.")

    async def _save_order_and_details(self, order_input: OrderInputDTO, details_input: List[OrderDetailInputDTO], contractor: Contractor) -> Tuple[Order, List[OrderDetail]]:
        order = await self._save_order(order_input, contractor)
        details = await self._save_details(details_input, order)

        return order, details

    async def _save_order(self, order_input: OrderInputDTO, contractor: Contractor) -> Order:
        order = await self.order_repository.save_order(
            order_input.to_order(contractor.contractor_id)
        )
        return order
    
    async def _save_details(self, details_input: List[OrderDetailInputDTO], order: Order) -> List[OrderDetail]:
        details = await self.order_detail_repository.create_details([
            det.to_order_detail(order.order_id) for det in details_input
        ])
        return details

    async def _notify_admins_on_new_order(self, order: Order, details: List[OrderDetail]):
        admins = await self.user_repository.get_admins()
        await self.admin_notification_service.send_new_order_notification(admins, order, details)

    async def get_order(self, order_id: int, contractor: Contractor) -> OrderOutputDTO | None:
        order = await self._get_order(order_id, contractor.contractor_id)
        if order is None:
            return None

        return OrderOutputDTO.from_order(order)
    
    async def _get_order(self, order_id: int, contractor_id: int) -> Order | None:
        return await self.order_repository.get_order_by_id_and_contractor_id(order_id, contractor_id)

    async def get_detailed_order(self, order_id: int, contractor: Contractor) -> DetailedOrderOutputDTO | None:
        detailed_order = await self._get_detailed_order(order_id, contractor.contractor_id)
        if detailed_order is None:
            return None

        return DetailedOrderOutputDTO.from_order(detailed_order)

    async def _get_detailed_order(self, order_id: int, contractor_id: int) -> DetailedOrder | None:
        return await self.order_repository.get_detailed_order_by_id_and_contractor_id(order_id, contractor_id)

    async def cancel_order(self, order_id: int, contractor: Contractor) -> OrderOutputDTO:
        # объявляем транзакцию
        async with self.transaction_manager:
            order = await self._get_order_and_check_order_access(order_id, contractor)

            self._check_order_can_be_cancelled(order)

            order, dropped_contractees = await self._cancel_order_and_drop_replies(order)

        # отправляем уведомление о отмене заказа привязанному администраторам 
        admin = await self.user_repository.get_admin_by_id(order.admin_id)
        await self.admin_notification_service.send_order_cancelled_notification(admin, order)
        
        if dropped_contractees:
            self.contractee_notification_service.send_order_cancelled_notification_many(dropped_contractees, order)

        return OrderOutputDTO.from_order(order)

    async def _get_order_and_check_order_access(self, order_id: int, contractor: Contractor) -> Order:
        """
        Получает заказ и проверяет может ли заказчик изменять заказ.
        """
        order = await self._get_order(order_id, contractor.contractor_id)

        if order is None:
            raise NotFoundException(order_id)
        
        if not OrderDomainService.is_owned_by(contractor.contractor_id):
            raise UnauthorizedAccessException()
        
        return order
    
    def _check_order_can_be_cancelled(self, order: Order):
        if order.status == OrderStatusEnum.fulfilled:
            raise OrderStatusChangeNotAllowedException(order.order_id, OrderStatusEnum.cancelled, "Заказ завершен")

    async def _cancel_order_and_drop_replies(self, order: Order) -> Tuple[Order, List[Contractee]]:
        old_status = order.status

        order = await self._change_order_status(order, OrderStatusEnum.cancelled)

        # Только подтвержденные заказы (не имеющие статус OrderStatusEnum.created) имеют отклики
        if old_status != OrderStatusEnum.created:
            dropped_contractees = await self._drop_order_replies(order)
            return order, dropped_contractees
        
        return order, []

    async def _change_order_status(self, order: Order, status: OrderStatusEnum) -> Order:
        return await self.order_repository.change_order_status(order.order_id, status)

    async def _drop_order_replies(self, order: Order) -> List[Contractee]:
        return await self.reply_repository.drop_order_replies_by_order_id(order.order_id)

    async def _send_notifications_on_order_cancel(self, order: Order, dropped_contractees: List[Contractee]):
        if order.admin_id:
            await self._notify_admin_on_order_cancelled(order)

        if dropped_contractees:
            await self._notify_contractees_on_order_cancelled(order, dropped_contractees)

    async def _notify_admin_on_order_cancelled(self, order: Order):
        admin = await self.user_repository.get_admin_by_id(order.admin_id)
        await self.admin_notification_service.send_order_cancelled_notification(admin, order)

    async def _notify_contractees_on_order_cancelled(self, order: Order, dropped_contractees: List[Contractee]):
        await self.contractee_notification_service.send_order_cancelled_notification_many(dropped_contractees, order)

    async def set_order_active(self, order_id: int, contractor: Contractor) -> OrderOutputDTO:
        # объявляем транзакцию
        async with self.transaction_manager:
            order = await self._get_order_and_check_order_access(order_id, contractor)

            approved_contractees = await self._check_order_can_be_set_active(order)

            order, dropped_contractees = await self._set_order_active_and_drop_replies(order)

        await self._send_notifications_on_order_set_active(order, approved_contractees, dropped_contractees)

        return OrderOutputDTO.from_order(order)

    async def _check_order_can_be_set_active(self, order: Order):
        if order.status != OrderStatusEnum.open or order.status != OrderStatusEnum.closed:
            raise OrderStatusChangeNotAllowedException(order.order_id, OrderStatusEnum.active, "Заказ не может быть перемещен в активное состояние")
        
        approved_contractees = await self._get_approved_contractees(order)
        if not approved_contractees:
            raise OrderStatusChangeNotAllowedException(order.order_id, OrderStatusEnum.active, "Отсутствуют подтвержденные отклики")

        return approved_contractees

    async def _get_approved_contractees(self, order: Order) -> List[Contractee]:
        return await self.reply_repository.get_approved_contractees_by_order_id(order.order_id)

    async def _set_order_active_and_drop_replies(self, order) -> Tuple[Order, List[Contractee]]:
        order = await self._change_order_status(order, OrderStatusEnum.active)
        dropped_contractees = await self._drop_unapproved_order_replies(order)
    
        return order, dropped_contractees

    async def _drop_unapproved_order_replies(self, order: Order) -> List[Contractee]:
        return await self.reply_repository.drop_unapproved_order_replies_by_order_id(order.order_id)

    async def _send_notifications_on_order_set_active(self, order: Order, approved_contractees: List[Contractee], dropped_contractees: List[Contractee]):
        await self._notify_admin_on_order_set_active(order)

        await self._notify_contractees_on_order_set_active(order, approved_contractees)

        if dropped_contractees:
            await self._notify_dropped_contractees(order, dropped_contractees)

    async def _notify_admin_on_order_set_active(self, order: Order):
        admin = await self.user_repository.get_admin_by_id(order.admin_id)
        await self.admin_notification_service.send_order_set_active_notification(admin, order)

    async def _notify_contractees_on_order_set_active(self, order: Order, approved_contractees: List[Contractee]):
        await self.contractee_notification_service.send_order_set_active_notification_many(approved_contractees, order)

    async def _notify_dropped_contractees(self, order: Order, dropped_contractees: List[Contractee]):
        await self.contractee_notification_service.send_reply_disapproved_notification_many(dropped_contractees, order)

    async def get_orders(self, contractor: Contractor, page: int = 1, size: int = 15) -> List[OrderOutputDTO]:
        orders = await self.order_repository.get_contractor_orders_by_page(contractor.contractor_id, page, size)
        return [OrderOutputDTO.from_order(order) for order in orders]

    async def get_detailed_orders(self, contractor: Contractor, page: int = 1, size: int = 15) -> List[DetailedOrderOutputDTO]:
        detailed_orders = await self.order_repository.get_contractor_detailed_orders_by_page(contractor.contractor_id, page, size)
        return [DetailedOrderOutputDTO.from_order(order) for order in detailed_orders]
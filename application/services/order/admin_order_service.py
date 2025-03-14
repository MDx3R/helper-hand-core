from typing import List, Tuple

from domain.models import Order, Admin, OrderDetail, Contractee, DetailedOrder
from domain.models.enums import OrderStatusEnum, RoleEnum, UserStatusEnum, GenderEnum

from domain.services.order import AdminOrderService
from domain.repositories import (
    UserRepository,
    OrderRepository, 
    OrderDetailRepository,
    ReplyRepository
)
from application.external.notification import (
    AdminNotificationService, 
    ContractorNotificationService,
    ContracteeNotificationService
)
from application.transactions import TransactionManager, transactional
from application.dtos.input import OrderInputDTO, OrderDetailInputDTO
from application.dtos.output import DetailedOrderOutputDTO, OrderOutputDTO

from domain.exceptions.service import (
    PermissionDeniedException,
    MissingOrderDetailsException, 
    OrderStatusChangeNotAllowedException, 
    UnauthorizedAccessException, 
    NotFoundException,
    OrderActionNotAllowedException
)
from domain.services.domain import OrderDomainService, AdminDomainService

class AdminOrderServiceImpl(AdminOrderService):
    def __init__(
        self, 
        user_repository: UserRepository,
        order_repository: OrderRepository, 
        order_detail_repository: OrderDetailRepository,
        reply_repository: ReplyRepository,
        transaction_manager: TransactionManager,
        admin_notification_service: AdminNotificationService, 
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

    async def create_order(self, order_input: OrderInputDTO, details_input: List[OrderDetailInputDTO], admin: Admin) -> DetailedOrderOutputDTO:
        self._check_order_can_be_created(order_input, details_input, admin)

        async with self.transaction_manager:
            order, details = await self._create_order_and_details(order_input, details_input, admin)

        await self._notify_contractees_on_new_order(order, details)

        return DetailedOrderOutputDTO.from_order_and_details(order, details)

    def _check_order_can_be_created(self, order_input: OrderInputDTO, details_input: List[OrderDetailInputDTO], admin: Admin):
        if not AdminDomainService.is_contractor(admin):
            raise PermissionDeniedException("Создание заказа", admin.admin_id)
        
        if not details_input:
            raise MissingOrderDetailsException("Отсутствуют сведения заказа.")

    async def _create_order_and_details(self, order_input: OrderInputDTO, details_input: List[OrderDetailInputDTO], admin: Admin) -> Tuple[Order, List[OrderDetail]]:
        order = await self._create_order(order_input, admin)
        details = await self._create_details(details_input, order)

        return order, details

    async def _create_order(self, order_input: OrderInputDTO, admin: Admin) -> Order:
        order = order_input.to_order(admin.admin_id)
        order.admin_id = admin.admin_id # устанавливаем куратора для заказа
        order.status = OrderStatusEnum.open # открываем заказ
        
        order = await self._save_order(order)
        
        return order
    
    async def _save_order(self, order: Order) -> Order:
        order = await self.order_repository.save_order(order)
        return order

    async def _create_details(self, details_input: List[OrderDetailInputDTO], order: Order) -> List[OrderDetail]:
        details = await self.order_detail_repository.create_details([
            det.to_order_detail(order.order_id) for det in details_input
        ])
        return details

    async def _notify_contractees_on_new_order(self, order: Order, details: List[OrderDetail]):
        contractees = await self._get_suitable_contractees_for_order(order, details)
        await self.contractee_notification_service.send_new_order_notification(contractees, order)

    async def _get_suitable_contractees_for_order(self, order: Order, details: List[OrderDetail]) -> List[Contractee]:
        contractees = await self.user_repository.filter_contractees_by(
            status=UserStatusEnum.registered, 
            gender=self._determine_required_gender_for_order(details)
        )
        return contractees

    def _determine_required_gender_for_order(self, details: List[OrderDetail]) -> GenderEnum | None:
        assert details, "details не должны быть пустыми"
        gender = details[0].gender
        for i in details:
            # если запрашивается хотя бы 2 каких либо отличных пола: 
            # GenderEnum.male и GenderEnum.female, GenderEnum.male и None, GenderEnum.female и None 
            # - все сочетания по 2 элемента из значений доступных для OrderDetail.gender
            # то возвращаем None (любой пол)
            if gender != i.gender:
                return None

        return gender

    async def get_order(self, order_id: int, admin: Admin) -> OrderOutputDTO | None:
        order = await self.order_repository.get_order_by_id(order_id)
        if order is None:
            return None

        return OrderOutputDTO.from_order(order)

    async def get_detailed_order(self, order_id: int, admin: Admin) -> DetailedOrderOutputDTO | None:
        detailed_order = await self.order_repository.get_detailed_order_by_id(order_id)
        if detailed_order is None:
            return None

        return DetailedOrderOutputDTO.from_order(detailed_order)

    async def take_order(self, order_id: int, admin: Admin) -> OrderOutputDTO:
        async with self.transaction_manager:
            order = await self._get_order_and_check_exists(order_id)
            self._check_order_can_be_assigned(order)
            order = await self._take_order(order, admin)

        await self._notify_contractor_on_admin_assigned(order)

        return OrderOutputDTO.from_order(order)

    async def _get_order_and_check_exists(self, order_id: int) -> Order:
        order = await self.order_repository.get_order_by_id(order_id)
        if order is None:
            raise NotFoundException(order_id)
        
        return order

    def _check_order_can_be_assigned(self, order: Order):
        if OrderDomainService.has_supervisor(order):
            raise OrderActionNotAllowedException(order.order_id, "Куратор назначен", "Назначить куратора")
        if not OrderDomainService.can_be_assigned(order):
            raise OrderActionNotAllowedException(order.order_id, OrderStatusEnum.created, "Назначить куратора")

    async def _take_order(self, order: Order, admin: Admin) -> Order:
        order.admin_id = admin.admin_id
        order = await self._save_order(order)
        return order

    async def _notify_contractor_on_admin_assigned(self, order: Order):
        contractor = await self.user_repository.get_contractor_by_id(order.contractor_id)
        await self.contractor_notification_service.send_admin_assigned_for_order_notification(contractor, order)

    async def approve_order(self, order_id: int, admin: Admin) -> OrderOutputDTO:
        async with self.transaction_manager:
            order = await self._get_detailed_order_and_check_exists(order_id)
            self._check_order_can_be_approved(order, admin)
            order = await self._approve_order(order, admin)

        await self._notify_contractor_on_order_approved(order)
        await self._notify_contractees_on_new_order(order, order.details)

        return OrderOutputDTO.from_order(order)

    def _check_order_can_be_approved(self, order: Order, admin: Admin):
        is_supervised = OrderDomainService.has_supervisor(order) and not OrderDomainService.is_supervised_by(order, admin.admin_id)
        if not is_supervised:
            raise UnauthorizedAccessException("Невозможно подтвердить чужой заказ.")

        if not OrderDomainService.can_be_approved(order):
            raise OrderStatusChangeNotAllowedException(order.order_id, OrderStatusEnum.open, "Заказ не может быть подтвержден")

    async def _get_detailed_order_and_check_exists(self, order_id: int) -> DetailedOrder:
        order = await self.order_repository.get_detailed_order_by_id(order_id)
        if order is None:
            raise NotFoundException(order_id)
        
        return order

    async def _approve_order(self, order: DetailedOrder, admin: Admin) -> DetailedOrder:
        order.admin_id = admin.admin_id
        order.status = OrderStatusEnum.open
        order = await self._save_order(order)
        return order

    async def _notify_contractor_on_order_approved(self, order: Order):
        contractor = await self.user_repository.get_contractor_by_id(order.contractor_id)
        await self.contractor_notification_service.send_order_approved_notification(contractor, order)

    async def cancel_order(self, order_id: int, admin: Admin) -> OrderOutputDTO:
        async with self.transaction_manager:
            order = await self._get_order_and_check_exists(order_id)
            self._check_order_can_be_cancelled(order, admin)
            order, dropped_contractees = await self._cancel_order_and_drop_replies(order)
        
        await self._notify_contractor_on_order_cancelled(order)

        if dropped_contractees:
            await self._notify_contractees_on_order_cancelled(order, dropped_contractees)

        return OrderOutputDTO.from_order(order)

    def _check_order_can_be_cancelled(self, order: Order, admin: Admin):
        is_supervised = OrderDomainService.has_supervisor(order) and not OrderDomainService.is_supervised_by(order, admin.admin_id)
        if is_supervised:
            raise UnauthorizedAccessException("Невозможно отменить чужой заказ.")
        
        if not OrderDomainService.can_be_cancelled(order):
            raise OrderStatusChangeNotAllowedException(order.order_id, OrderStatusEnum.cancelled, f"Заказ имеет статус {order.status}")

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

    async def _notify_contractor_on_order_cancelled(self, order: Order):
        contractor = await self.user_repository.get_contractor_by_id(order.contractor_id)
        await self.contractor_notification_service.send_order_cancelled_notification(contractor, order)

    async def _notify_contractees_on_order_cancelled(self, order: Order, dropped_contractees: List[Contractee]):
        await self.contractee_notification_service.send_order_cancelled_notification_many(dropped_contractees, order)

    async def lock_order(self, order_id: int, admin: Admin) -> OrderOutputDTO:
        async with self.transaction_manager:
            order = await self._get_order_and_check_exists(order_id)
            self._check_order_can_be_closed(order, admin)
            order = await self._lock_order(order)

        await self._notify_contractor_on_order_closed(order)

        return OrderOutputDTO.from_order(order)

    def _check_order_can_be_closed(self, order: Order, admin: Admin):
        if not OrderDomainService.is_supervised_by(order, admin.admin_id):
            raise UnauthorizedAccessException("Невозможно закрыть чужой заказ.")
        
        if not OrderDomainService.can_be_closed(order):
            raise OrderStatusChangeNotAllowedException(order.order_id, OrderStatusEnum.closed, "Заказ не может быть закрыт")

    async def _lock_order(self, order: Order) -> Order:
        return await self._change_order_status(order, OrderStatusEnum.closed)

    async def _notify_contractor_on_order_closed(self, order: Order):
        contractor = await self.user_repository.get_contractor_by_id(order.contractor_id)
        await self.contractor_notification_service.send_order_closed_notification(contractor, order)

    async def open_order(self, order_id: int, admin: Admin) -> OrderOutputDTO:
        async with self.transaction_manager:
            order = await self._get_order_and_check_exists(order_id)
            self._check_order_can_be_opened(order, admin)
            order = await self._open_order(order)

        await self._notify_contractor_on_order_opened(order)

        return OrderOutputDTO.from_order(order)

    def _check_order_can_be_opened(self, order: Order, admin: Admin):
        if not OrderDomainService.is_supervised_by(order, admin.admin_id):
            raise UnauthorizedAccessException("Невозможно открыть чужой заказ.")
        
        if not OrderDomainService.can_be_opened(order):
            raise OrderStatusChangeNotAllowedException(order.order_id, OrderStatusEnum.open, "Заказ не может быть открыт")

    async def _open_order(self, order: Order) -> Order:
        return await self._change_order_status(order, OrderStatusEnum.open)

    async def _notify_contractor_on_order_opened(self, order: Order):
        contractor = await self.user_repository.get_contractor_by_id(order.contractor_id)
        await self.contractor_notification_service.send_order_opened_notification(contractor, order)

    async def fulfill_order(self, order_id: int, admin: Admin) -> OrderOutputDTO:
        async with self.transaction_manager:
            order = await self._get_order_and_check_exists(order_id)
            self._check_order_can_be_fulfilled(order, admin)
            order = await self._fulfill_order(order)

        await self._notify_contractor_on_order_fulfilled(order)

        return OrderOutputDTO.from_order(order)

    def _check_order_can_be_fulfilled(self, order: Order, admin: Admin):
        if not OrderDomainService.is_supervised_by(order, admin.admin_id):
            raise UnauthorizedAccessException("Невозможно завершить чужой заказ.")
        
        if not OrderDomainService.can_be_fulfilled(order):
            raise OrderStatusChangeNotAllowedException(order.order_id, OrderStatusEnum.fulfilled, "Заказ не может быть завершен")

    async def _fulfill_order(self, order: Order) -> Order:
        return await self._change_order_status(order, OrderStatusEnum.fulfilled)

    async def _notify_contractor_on_order_fulfilled(self, order: Order):
        contractor = await self.user_repository.get_contractor_by_id(order.contractor_id)
        await self.contractor_notification_service.send_order_fulfilled_notification(contractor, order)

    async def get_orders(self, admin: Admin, page: int = 1, size: int = 15) -> List[OrderOutputDTO]:
        orders = await self.order_repository.get_orders_by_page(page, size)
        return [OrderOutputDTO.from_order(order) for order in orders]

    async def get_detailed_orders(self, admin: Admin, page: int = 1, size: int = 15) -> List[DetailedOrderOutputDTO]:
        detailed_orders = await self.order_repository.get_detailed_orders_by_page(page, size)
        return [DetailedOrderOutputDTO.from_order(order) for order in detailed_orders]

    async def get_one_unassigned_order(self, admin: Admin, last_order_id: int = None) -> DetailedOrderOutputDTO | None:
        detailed_order = (await self.order_repository.get_detailed_unassigned_orders_by_last_order_id(last_order_id, 1))[0]
        return DetailedOrderOutputDTO.from_order(detailed_order)

    async def get_open_orders(self, admin: Admin, page: int = 1, size: int = 15) -> List[OrderOutputDTO]:
        orders = await self.order_repository.get_open_orders_by_page(page, size)
        return [OrderOutputDTO.from_order(order) for order in orders]

    async def get_closed_orders(self, admin: Admin, page: int = 1, size: int = 15) -> List[OrderOutputDTO]:
        orders = await self.order_repository.get_closed_orders_by_page(page, size)
        return [OrderOutputDTO.from_order(order) for order in orders]

    async def get_active_orders(self, admin: Admin, page: int = 1, size: int = 15) -> List[OrderOutputDTO]:
        orders = await self.order_repository.get_active_orders_by_page(page, size)
        return [OrderOutputDTO.from_order(order) for order in orders]

    async def get_contractee_orders(self, contractee_id: int, admin: Admin, page: int = 1, size: int = 15) -> List[OrderOutputDTO]:
        orders = await self.order_repository.get_contractee_orders_by_page(contractee_id, page, size)
        return [OrderOutputDTO.from_order(order) for order in orders]

    async def get_contractor_orders(self, contractor_id: int, admin: Admin, page: int = 1, size: int = 15) -> List[OrderOutputDTO]:
        orders = await self.order_repository.get_contractor_orders_by_page(contractor_id, page, size)
        return [OrderOutputDTO.from_order(order) for order in orders]

    async def get_admin_orders(self, admin_id: int, admin: Admin, page: int = 1, size: int = 15) -> List[OrderOutputDTO]:
        orders = await self.order_repository.get_admin_orders_by_page(admin_id, page, size)
        return [OrderOutputDTO.from_order(order) for order in orders]
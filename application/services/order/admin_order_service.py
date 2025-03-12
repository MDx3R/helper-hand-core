from typing import List

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
    MissingOrderDetailsException, 
    OrderStatusChangeNotAllowedException, 
    UnauthorizedAccessException, 
    NotFoundException
)

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
        if len(details_input) == 0:
            raise MissingOrderDetailsException("Отсутствуют сведения заказа.")
        
        async with self.transaction_manager:
            order = order_input.to_order(admin.admin_id)
            order.admin_id = admin.admin_id # устанавливаем куратора для заказа
            order.status = OrderStatusEnum.open # открываем заказ
            
            order = await self.order_repository.save_order(order)

            details = await self.order_detail_repository.create_details([
                det.to_order_detail(order.order_id) for det in details_input
            ]) 

        await self._notify_contractees_on_new_order(order, details)

        return DetailedOrderOutputDTO.from_order_and_details(order, details)
    
    async def _notify_contractees_on_new_order(self, order: Order, details: List[OrderDetail]):
        contractees = await self._get_suitable_contractees_for_order(order, details)
        await self.contractee_notification_service.send_new_order_notification(contractees, order)

    async def _get_suitable_contractees_for_order(self, order: Order, details: List[OrderDetail]) -> List[Contractee]:
        contractees = await self.user_repository.filter_users_by(
            role=RoleEnum.contractee, 
            status=UserStatusEnum.registered, 
            gender=self._determine_required_gender_for_order(details)
        )
        return contractees

    def _determine_required_gender_for_order(self, details: List[OrderDetail]) -> GenderEnum | None:
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
            order = await self.order_repository.get_order_by_id(order_id)
            if order is None:
                raise NotFoundException(order_id)

            order.admin_id = admin.admin_id

            order = await self.order_repository.save_order(order)

        contractor = await self.user_repository.get_contractor_by_id(order.contractor_id)
        await self.contractor_notification_service.send_admin_assigned_for_order_notification(contractor, order)

        return OrderOutputDTO.from_order(order)

    async def approve_order(self, order_id: int, admin: Admin) -> OrderOutputDTO:
        async with self.transaction_manager:
            order = await self.order_repository.get_detailed_order_by_id(order_id)
            if order is None:
                raise NotFoundException(order_id)

            if order.status != OrderStatusEnum.created:
                raise OrderStatusChangeNotAllowedException(order_id, OrderStatusEnum.open, "Заказ не может быть подтвержден")

            await self.order_repository.change_order_status(order_id, OrderStatusEnum.open)
            order.status = OrderStatusEnum.open

        contractor = await self.user_repository.get_contractor_by_id(order.contractor_id)
        await self.contractor_notification_service.send_order_approved_notification(contractor, order)

        await self._notify_contractees_on_new_order(order, order.details)

        return OrderOutputDTO.from_order(order)

    async def cancel_order(self, order_id: int, admin: Admin) -> OrderOutputDTO:
        async with self.transaction_manager:
            order = await self.order_repository.get_order_by_id(order_id)
            if order is None:
                raise NotFoundException(order_id)

            if order.status != OrderStatusEnum.created and order.admin_id != admin.admin_id:
                raise UnauthorizedAccessException()

            if order.status == OrderStatusEnum.fulfilled:
                raise OrderStatusChangeNotAllowedException(order_id, OrderStatusEnum.cancelled, "Заказ завершен")

            old_status = order.status

            order = await self.order_repository.change_order_status(order_id, OrderStatusEnum.cancelled)

            if old_status != OrderStatusEnum.created:
                dropped_contractees = await self.reply_repository.drop_order_replies_by_order_id(order_id)

        contractor = await self.user_repository.get_contractor_by_id(order.contractor_id)
        await self.contractor_notification_service.send_order_cancelled_notification(contractor, order)
        
        if old_status != OrderStatusEnum.created:
            self.contractee_notification_service.send_order_cancelled_notification_many(dropped_contractees, order)

        return OrderOutputDTO.from_order(order)

    async def lock_order(self, order_id: int, admin: Admin) -> OrderOutputDTO:
        async with self.transaction_manager:
            order = await self.order_repository.get_order_by_id(order_id)
            if order is None:
                raise NotFoundException(order_id)

            if order.admin_id != admin.admin_id:
                raise UnauthorizedAccessException()

            if order.status != OrderStatusEnum.open:
                raise OrderStatusChangeNotAllowedException(order_id, OrderStatusEnum.closed, "Заказ не может быть закрыт")

            order = await self.order_repository.change_order_status(order_id, OrderStatusEnum.closed)

        contractor = await self.user_repository.get_contractor_by_id(order.contractor_id)
        await self.contractor_notification_service.send_order_closed_notification(contractor, order)

        return OrderOutputDTO.from_order(order)

    async def unlock_order(self, order_id: int, admin: Admin) -> OrderOutputDTO:
        async with self.transaction_manager:
            order = await self.order_repository.get_order_by_id(order_id)
            if order is None:
                raise NotFoundException(order_id)

            if order.admin_id != admin.admin_id:
                raise UnauthorizedAccessException()

            if order.status != OrderStatusEnum.closed:
                raise OrderStatusChangeNotAllowedException(order_id, OrderStatusEnum.open, "Заказ не может быть открыт")

            order = await self.order_repository.change_order_status(order_id, OrderStatusEnum.open)

        contractor = await self.user_repository.get_contractor_by_id(order.contractor_id)
        await self.contractor_notification_service.send_order_opened_notification(contractor, order)

        return OrderOutputDTO.from_order(order)

    async def fulfill_order(self, order_id: int, admin: Admin) -> OrderOutputDTO:
        async with self.transaction_manager:
            order = await self.order_repository.get_order_by_id(order_id)
            if order is None:
                raise NotFoundException(order_id)

            if order.admin_id != admin.admin_id:
                raise UnauthorizedAccessException()

            if order.status != OrderStatusEnum.active:
                raise OrderStatusChangeNotAllowedException(order_id, OrderStatusEnum.fulfilled, "Заказ не может быть завершен")

            order = await self.order_repository.change_order_status(order_id, OrderStatusEnum.fulfilled)

        contractor = await self.user_repository.get_contractor_by_id(order.contractor_id)
        await self.contractor_notification_service.send_order_fulfilled_notification(contractor, order)

        return OrderOutputDTO.from_order(order)

    async def get_orders(self, admin: Admin, page: int = 1, size: int = 15) -> List[OrderOutputDTO]:
        orders = await self.order_repository.get_orders_by_page(page, size)
        return [OrderOutputDTO.from_order(order) for order in orders]

    async def get_detailed_orders(self, admin: Admin, page: int = 1, size: int = 15) -> List[DetailedOrderOutputDTO]:
        detailed_orders = await self.order_repository.get_detailed_orders_by_page(page, size)
        return [DetailedOrderOutputDTO.from_order(order) for order in detailed_orders]

    async def get_one_unassigned_order(self, admin: Admin, last_order_id: int = None) -> DetailedOrderOutputDTO | None:
        detailed_order = await self.order_repository.get_detailed_unassigned_orders_by_last_order_id(last_order_id, 1)[0]
        
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
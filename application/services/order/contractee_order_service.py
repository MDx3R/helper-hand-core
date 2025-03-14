from typing import List
from abc import ABC, abstractmethod

from datetime import timedelta

from domain.models import Contractee, OrderDetail
from domain.models.enums import OrderStatusEnum

from domain.repositories import OrderRepository, OrderDetailRepository, UserRepository, ReplyRepository
from application.external.notification import AdminNotificationService, ContracteeNotificationService
from application.dtos.input import OrderInputDTO, OrderDetailInputDTO
from application.dtos.output import DetailedOrderOutputDTO, OrderOutputDTO, OrderDetailOutputDTO
from application.transactions import TransactionManager, transactional

from domain.time import get_current_time, is_current_time_valid_for_reply
from domain.services.order import ContracteeOrderService

class ContracteeOrderServiceImpl(ContracteeOrderService):
    """
    Класс реализации интерфейса `ContractorOrderService` для работы исполнителя с заказами.

    Attributes:
        user_repository (UserRepository): Репозиторий с данными пользователей.
        order_repository (OrderRepository): Репозиторий с данными заказов.
        order_detail_repository (OrderDetailRepository): Репозиторий с данными сведений заказов.
        reply_repository (ReplyRepository): Репозиторий с данными откликов.
        transaction_manager (TransactionManager): Менеджер транзакций.
    """

    def __init__(
        self, 
        user_repository: UserRepository,
        order_repository: OrderRepository, 
        order_detail_repository: OrderDetailRepository,
        reply_repository: ReplyRepository,
        transaction_manager: TransactionManager,
    ):
        self.user_repository = user_repository
        self.order_repository = order_repository
        self.order_detail_repository = order_detail_repository
        self.reply_repository = reply_repository
        self.transaction_manager = transaction_manager
    
    async def get_order(self, order_id: int, contractee: Contractee) -> DetailedOrderOutputDTO | None:
        detailed_order = await self.order_repository.get_detailed_order_by_id(order_id)
        if detailed_order.status == OrderStatusEnum.open:
            return DetailedOrderOutputDTO.from_order(detailed_order)
        if await self.reply_repository.has_contractee_replied_to_order(order_id, contractee.contractee_id):
            return DetailedOrderOutputDTO.from_order(detailed_order)

        return None

    async def get_one_open_order(self, contractee: Contractee, last_order_id: int = None) -> DetailedOrderOutputDTO | None:
        detailed_order = (await self.order_repository.get_detailed_open_orders_by_last_order_id(last_order_id, 1))[0]
        return DetailedOrderOutputDTO.from_order(detailed_order)
    
    async def get_open_orders(self, contractee: Contractee, page: int = 1, size: int = 15) -> List[OrderOutputDTO]:
        detailed_orders = await self.order_repository.get_detailed_open_orders_by_page(page, size)
        return [DetailedOrderOutputDTO.from_order(order) for order in detailed_orders]

    async def get_contractee_orders(self, contractee: Contractee, page: int = 1, size: int = 15) -> List[OrderOutputDTO]:
        orders = await self.order_repository.get_contractee_orders_by_page(contractee.contractee_id, page, size)
        return [OrderOutputDTO.from_order(order) for order in orders]
    
    async def get_available_details(self, order_id: int, contractee: Contractee) -> List[OrderDetailInputDTO]:
        async with self.transaction_manager:
            order = await self.order_repository.get_order_by_id(order_id)
            if order.status != OrderStatusEnum.open:
                return []

            unfiltered_details = await self.order_detail_repository.get_available_details_by_order_id(order_id)
            details = await self._filter_available_details_for_contractee(contractee, unfiltered_details)

        return [OrderDetailInputDTO.to_order_detail(detail) for detail in details]
    
    async def _filter_available_details_for_contractee(self, contractee: Contractee, details: List[OrderDetail]) -> List[OrderDetail]:
        busy_dates = await self.reply_repository.get_contractee_approved_future_busy_dates(contractee.contractee_id)
        taken_details = [reply.detail_id for reply in await self.reply_repository.get_contractee_future_replies(contractee.contractee_id)]

        filtered_details = []
        for detail in details:
            if not is_current_time_valid_for_reply(detail.start_date):
                continue
            if detail.gender and detail.gender != contractee.gender:
                continue
            if detail.detail_id in taken_details:
                continue
            if detail.date in busy_dates:
                continue

            filtered_details.append(detail)

        return filtered_details
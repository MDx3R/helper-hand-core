from typing import List, Tuple

from domain.dto.common import DetailedOrderDTO
from domain.dto.context import UserContextDTO
from domain.dto.input import OrderDetailInputDTO, OrderInputDTO
from domain.dto.internal.order import CreateOrderDTO
from domain.entities.order import Order
from domain.entities.order_detail import OrderDetail
from domain.repositories.order_detail_repository import OrderDetailRepository
from domain.repositories.order_repository import OrderRepository


class CreateOrderUseCase:
    def __init__(
        self,
        order_repository: OrderRepository,
        order_detail_repository: OrderDetailRepository,
    ):
        self.order_repository = order_repository
        self.order_detail_repository = order_detail_repository

    async def create_order(self, request: CreateOrderDTO) -> DetailedOrderDTO:
        order, details = await self._save_order_and_details(request)
        return DetailedOrderDTO.from_order_and_details(order, details)

    async def _save_order_and_details(
        self,
        request: CreateOrderDTO,
    ) -> Tuple[Order, List[OrderDetail]]:
        order = await self._save_order(request.order, request.context)
        details = await self._save_details(request.details, order)

        return order, details

    async def _save_order(
        self, order_input: OrderInputDTO, context: UserContextDTO
    ) -> Order:
        order = await self.order_repository.save(
            self._get_order_entity(order_input, context)
        )
        return order

    def _get_order_entity(
        self, order_input: OrderInputDTO, context: UserContextDTO
    ) -> Order:
        return order_input.to_order(context.user_id)

    async def _save_details(
        self, details_input: List[OrderDetailInputDTO], order: Order
    ) -> List[OrderDetail]:
        details = await self.order_detail_repository.create_details(
            [det.to_order_detail(order.order_id) for det in details_input]
        )
        return details


class CreateAdminOrderUseCase(CreateOrderUseCase):
    def _get_order_entity(
        self, order_input: OrderInputDTO, context: UserContextDTO
    ) -> Order:
        order = order_input.to_order(context.user_id)
        order.admin_id = context.user_id
        return order

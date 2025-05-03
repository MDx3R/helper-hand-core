from typing import List

from application.transactions import transactional
from domain.dto.order.request.create_order_dto import CreateOrderDTO
from domain.dto.order.request.order_input_dto import (
    OrderDetailInputDTO,
    OrderInputDTO,
)
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.entities.order.composite_order import OrderWithDetails
from domain.entities.order.detail import OrderDetail
from domain.entities.order.order import Order
from domain.mappers.order_mappers import OrderDetailMapper, OrderMapper
from domain.repositories.order.detail.order_detail_command_repository import (
    OrderDetailCommandRepository,
)
from domain.repositories.order.order_command_repository import (
    OrderCommandRepository,
)
from domain.wager import calculate_pay


class CreateOrderWithDetailsUseCase:
    def __init__(
        self,
        order_repository: OrderCommandRepository,
        detail_repository: OrderDetailCommandRepository,
    ):
        self.order_repository = order_repository
        self.detail_repository = detail_repository

    @transactional
    async def execute(self, request: CreateOrderDTO) -> OrderWithDetails:
        order = await self._save_order_and_details(request)
        return OrderMapper.to_output_with_details(order)

    async def _save_order_and_details(
        self,
        request: CreateOrderDTO,
    ) -> OrderWithDetails:
        order = await self._save_order(request.order, request.context)
        details = await self._save_details(request.details, order)

        return OrderWithDetails(order=order, details=details)

    async def _save_order(
        self, order_input: OrderInputDTO, context: UserContextDTO
    ) -> Order:
        return await self.order_repository.create_order(
            self._build_order(order_input, context)
        )

    def _build_order(
        self, order_input: OrderInputDTO, context: UserContextDTO
    ) -> Order:
        return OrderMapper.from_input(order_input, context.user_id)

    async def _save_details(
        self, details_input: List[OrderDetailInputDTO], order: Order
    ) -> List[OrderDetail]:
        return await self.detail_repository.create_details(
            self._build_details(details_input, order)
        )

    def _build_details(
        self, details_input: List[OrderDetailInputDTO], order: Order
    ) -> List[OrderDetail]:
        return [
            OrderDetailMapper.from_input(
                i, order.order_id, fee=i.wager - calculate_pay(i.wager)
            )
            for i in details_input
        ]

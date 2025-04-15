from typing import List, Tuple

from application.transactions import transactional
from domain.dto.common import (
    DetailedOrderDTO,
    OrderDetailDTO,
    OrderDTO,
    detailed_order_dto,
)
from domain.dto.context import UserContextDTO
from domain.dto.input import OrderDetailInputDTO, OrderInputDTO
from domain.dto.internal import (
    CreateOrderDetailDTO,
    CreateOrderDetailsDTO,
    CreateOrderDTO,
)
from domain.entities import Order, OrderDetail
from domain.repositories import OrderDetailRepository, OrderRepository
from domain.wager import calculate_wager


class CreateOrderDetailsUseCase:
    def __init__(
        self,
        order_detail_repository: OrderDetailRepository,
    ):
        self.order_detail_repository = order_detail_repository

    @transactional
    async def create_detail(
        self, request: CreateOrderDetailDTO
    ) -> OrderDetailDTO:
        detail = await self._save_detail(request.detail, request.order)
        return OrderDetailDTO.from_order_detail(detail)

    @transactional
    async def create_details(
        self, request: CreateOrderDetailsDTO
    ) -> List[OrderDetailDTO]:
        details = await self._save_details(request.details, request.order)
        return [OrderDetailDTO.from_order_detail(d) for d in details]

    async def _save_detail(
        self, detail_input: OrderDetailInputDTO, order: OrderDTO
    ) -> List[OrderDetail]:
        detail = await self.order_detail_repository.create_detail(
            detail_input.to_order_detail(
                order.order_id, self.calculate_fee(detail)
            )
        )
        return detail

    async def _save_details(
        self, details_input: List[OrderDetailInputDTO], order: OrderDTO
    ) -> List[OrderDetail]:
        details = await self.order_detail_repository.create_details(
            [
                det.to_order_detail(order.order_id, self.calculate_fee(det))
                for det in details_input
            ]
        )
        return details

    def calculate_fee(self, detail: OrderDetailInputDTO) -> int:
        return detail.wager - calculate_wager(detail.wager)


class CreateOrderUseCase:
    def __init__(
        self,
        order_repository: OrderRepository,
        create_details_use_case: CreateOrderDetailsUseCase,
    ):
        self.order_repository = order_repository
        self.create_details_use_case = create_details_use_case

    @transactional
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
        details = await self.create_details_use_case.create_details(
            CreateOrderDetailsDTO(
                order=OrderDTO.from_order(order), details=details_input
            )
        )
        return [det.to_order_detail() for det in details]


class CreateAdminOrderUseCase(CreateOrderUseCase):
    def _get_order_entity(
        self, order_input: OrderInputDTO, context: UserContextDTO
    ) -> Order:
        order = order_input.to_order(context.user_id)
        order.admin_id = context.user_id
        return order

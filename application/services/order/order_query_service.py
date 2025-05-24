from typing import List

from application.usecases.order.order_query_use_case import (
    GetOrderUseCase,
    ListOrdersUseCase,
    ListRecentOrdersUseCase,
)
from domain.dto.base import LastObjectDTO, PaginationDTO
from domain.dto.order.internal.order_query_dto import GetOrderDTO
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderOutputDTO,
)
from domain.dto.user.internal.user_context_dto import PaginatedDTO
from domain.services.order.order_service import OrderQueryService


class OrderQueryServiceImpl(OrderQueryService):
    def __init__(
        self,
        list_recent_orders_use_case: ListRecentOrdersUseCase,
    ):
        self.list_recent_orders_use_case = list_recent_orders_use_case

    async def get_recent_orders(
        self, query: PaginationDTO
    ) -> List[OrderOutputDTO]:
        return await self.list_recent_orders_use_case.execute(query)


class BaseOrderQueryService:
    def __init__(
        self,
        get_order_use_case: GetOrderUseCase,
        get_orders_use_case: ListOrdersUseCase,
    ):
        self.get_order_use_case = get_order_use_case
        self.get_orders_use_case = get_orders_use_case

    async def get_order(
        self, query: GetOrderDTO
    ) -> CompleteOrderOutputDTO | None:
        return await self.get_order_use_case.execute(query)

    async def get_orders(self, query: PaginatedDTO) -> List[OrderOutputDTO]:
        return await self.get_orders_use_case.execute(query)

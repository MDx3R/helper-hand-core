from typing import List
from domain.dto.base import LastObjectDTO
from domain.dto.order.internal.order_filter_dto import OrderFilterDTO
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderOutputDTO,
)
from domain.dto.user.internal.user_context_dto import PaginatedDTO
from domain.mappers.order_mappers import OrderMapper
from domain.repositories.order.composite_order_query_repository import (
    CompositeOrderQueryRepository,
)
from domain.repositories.order.order_query_repository import (
    OrderQueryRepository,
)


class GetUnassignedOrderUseCase:
    def __init__(
        self,
        repository: CompositeOrderQueryRepository,
    ):
        self.repository = repository

    async def execute(
        self, query: LastObjectDTO
    ) -> CompleteOrderOutputDTO | None:
        orders = await self.repository.filter_complete_orders(
            OrderFilterDTO(last_id=query.last_id, admin_id=None, size=1)
        )
        if not orders:
            return None

        return OrderMapper.to_complete(orders[0])


class ListUnassignedOrdersUseCase:
    def __init__(
        self,
        repository: OrderQueryRepository,
    ):
        self.repository = repository

    async def execute(self, query: PaginatedDTO) -> List[OrderOutputDTO]:
        orders = await self.repository.filter_orders(
            OrderFilterDTO(
                last_id=query.last_id, admin_id=None, size=query.size
            )
        )

        return [OrderMapper.to_output(i) for i in orders]

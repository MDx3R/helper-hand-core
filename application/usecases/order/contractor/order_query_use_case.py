from domain.dto.order.internal.order_filter_dto import OrderFilterDTO
from domain.dto.order.internal.order_query_dto import GetOrderDTO
from domain.dto.order.response.order_output_dto import CompleteOrderOutputDTO
from domain.mappers.order_mappers import OrderMapper
from domain.repositories.order.composite_order_query_repository import (
    CompositeOrderQueryRepository,
)


class GetCompleteOrderForContractorUseCase:
    def __init__(
        self,
        repository: CompositeOrderQueryRepository,
    ):
        self.repository = repository

    async def execute(
        self, query: GetOrderDTO
    ) -> CompleteOrderOutputDTO | None:
        orders = await self.repository.filter_complete_orders(
            OrderFilterDTO(
                order_id=query.order_id, contractor_id=query.context.user_id
            )
        )

        if not orders:
            return None

        return OrderMapper.to_complete(orders[0])

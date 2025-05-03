from typing import List

from domain.dto.order.internal.order_filter_dto import OrderFilterDTO
from domain.dto.order.internal.order_query_dto import (
    GetOrderDTO,
    GetUserOrdersDTO,
)
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderOutputDTO,
    OrderWithDetailsOutputDTO,
)
from domain.mappers.order_mappers import OrderMapper
from domain.repositories.order.composite_order_query_repository import (
    CompositeOrderQueryRepository,
)
from domain.repositories.order.order_query_repository import (
    OrderQueryRepository,
)


# Common
class GetOrderUseCase:
    def __init__(
        self,
        repository: OrderQueryRepository,
    ):
        self.repository = repository

    async def execute(self, query: GetOrderDTO) -> OrderOutputDTO | None:
        order = await self.repository.get_order(query)
        if not order:
            return None

        return OrderMapper.to_output(order)


class GetOrderWithDetailsUseCase:
    def __init__(
        self,
        repository: CompositeOrderQueryRepository,
    ):
        self.repository = repository

    async def execute(
        self, query: GetOrderDTO
    ) -> OrderWithDetailsOutputDTO | None:
        order = await self.repository.get_order_with_details(query)
        if not order:
            return None

        return OrderMapper.to_output_with_details(order)


class GetCompleteOrderUseCase:
    def __init__(
        self,
        repository: CompositeOrderQueryRepository,
    ):
        self.repository = repository

    async def execute(
        self, query: GetOrderDTO
    ) -> CompleteOrderOutputDTO | None:
        order = await self.repository.get_complete_order(query)
        if not order:
            return None

        return OrderMapper.to_complete(order)


# User's
class ListAdminOrdersUseCase:
    def __init__(
        self,
        repository: OrderQueryRepository,
    ):
        self.repository = repository

    async def execute(self, query: GetUserOrdersDTO) -> List[OrderOutputDTO]:
        orders = await self.repository.filter_orders(
            OrderFilterDTO(
                admin_id=query.user_id,
                last_id=query.last_id,
                size=query.size,
                order="descending",
            )
        )

        return [OrderMapper.to_output(i) for i in orders]


class ListContractorOrdersUseCase:
    def __init__(
        self,
        repository: OrderQueryRepository,
    ):
        self.repository = repository

    async def execute(self, query: GetUserOrdersDTO) -> List[OrderOutputDTO]:
        orders = await self.repository.filter_orders(
            OrderFilterDTO(
                contractor_id=query.user_id,
                last_id=query.last_id,
                size=query.size,
                order="descending",
            )
        )

        return [OrderMapper.to_output(i) for i in orders]


class ListContracteeOrdersUseCase:
    def __init__(
        self,
        repository: OrderQueryRepository,
    ):
        self.repository = repository

    async def execute(self, query: GetUserOrdersDTO) -> List[OrderOutputDTO]:
        orders = await self.repository.filter_orders(
            OrderFilterDTO(
                contractee_id=query.user_id,
                last_id=query.last_id,
                size=query.size,
                order="descending",
            )
        )

        return [OrderMapper.to_output(i) for i in orders]

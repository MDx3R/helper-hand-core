from dataclasses import dataclass
from typing import List, Optional

from sqlalchemy import Select

from domain.dto.order.internal.order_filter_dto import OrderFilterDTO
from domain.entities.order.composite_order import (
    CompleteOrder,
    OrderWithDetails,
)
from domain.entities.order.detail import OrderDetail
from domain.entities.order.order import Order
from domain.entities.user.admin.admin import Admin
from domain.entities.user.contractor.contractor import Contractor
from domain.repositories.order.composite_order_query_repository import (
    CompositeOrderQueryRepository,
)
from infrastructure.database.mappers import (
    AdminMapper,
    ContractorMapper,
    OrderDetailMapper,
    OrderMapper,
)
from infrastructure.repositories.base import O, QueryExecutor
from infrastructure.repositories.order.base import (
    OrderQueryBuilder,
    UnmappedOrder,
)


@dataclass
class OrderAggregator:
    order: Order
    details: List[OrderDetail]
    contractor: Optional[Contractor] = None
    admin: Optional[Admin] = None


class CompositeOrderQueryRepositoryImpl(CompositeOrderQueryRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def get_order_with_details(
        self, order_id: int
    ) -> OrderWithDetails | None:
        query_builder = self._get_order_with_details_builder()
        stmt = query_builder.where_order_id(order_id).build()

        return await self._execute_one_order_to_entity(stmt, OrderWithDetails)

    async def get_order_with_free_details(
        self, order_id: int
    ) -> OrderWithDetails | None:
        query_builder = self._get_order_with_details_builder()
        stmt = (
            query_builder.where_order_id(order_id)
            .apply_only_available_details()
            .build()
        )

        return await self._execute_one_order_to_entity(stmt, OrderWithDetails)

    async def get_complete_order(self, order_id: int) -> CompleteOrder | None:
        query_builder = self._get_complete_order_builder()
        stmt = query_builder.where_order_id(order_id).build()

        return await self._execute_one_order_to_entity(stmt, CompleteOrder)

    async def filter_orders_with_details(
        self, query: OrderFilterDTO
    ) -> List[OrderWithDetails]:
        query_builder = self._get_order_with_details_builder()
        stmt = query_builder.apply_order_filter(query).build()

        return await self._execute_many_orders_to_entity(
            stmt, OrderWithDetails
        )

    async def filter_complete_orders(
        self, query: OrderFilterDTO
    ) -> List[CompleteOrder]:
        query_builder = self._get_complete_order_builder()
        stmt = query_builder.apply_order_filter(query).build()

        return await self._execute_many_orders_to_entity(stmt, CompleteOrder)

    def _get_order_with_details_builder(self) -> OrderQueryBuilder:
        return self._get_query_buider().add_detail()

    def _get_complete_order_builder(self) -> OrderQueryBuilder:
        return (
            self._get_query_buider().add_detail().add_admin().add_contractor()
        )

    def _get_query_buider(self) -> OrderQueryBuilder:
        return OrderQueryBuilder()

    async def _execute_one_order_to_entity(
        self, statement: Select, cls: type[O]
    ) -> O | None:
        aggregator = await self._execute_one_order(statement)
        if not aggregator:
            return None

        return self._build_entity(cls, aggregator)

    async def _execute_many_orders_to_entity(
        self, statement: Select, cls: type[O]
    ) -> List[O]:
        aggregated = await self._execute_many_orders(statement)
        return [self._build_entity(cls, i) for i in aggregated]

    def _build_entity(self, cls: type[O], aggregator: OrderAggregator) -> O:
        return cls(
            order=aggregator.order,
            details=aggregator.details,
            contractor=aggregator.contractor,
            admin=aggregator.admin,
        )

    async def _execute_one_order(
        self, statement: Select
    ) -> OrderAggregator | None:
        unmapped_orders = await self._execute_many(statement)

        aggregator: OrderAggregator | None = None
        for unmapped in unmapped_orders:
            if not aggregator:
                aggregator = self._aggregator_from_unmapped_and_order(unmapped)
            else:
                aggregator.details.append(
                    OrderDetailMapper.to_model(unmapped.detail)
                )

        return aggregator

    async def _execute_many_orders(
        self, statement: Select
    ) -> List[OrderAggregator]:
        unmapped_orders = await self._execute_many(statement)
        aggregated: dict[int, OrderAggregator] = {}
        for unmapped in unmapped_orders:
            order = unmapped.order
            if order.order_id not in aggregated:
                aggregated[order.order_id] = (
                    self._aggregator_from_unmapped_and_order(unmapped)
                )
            else:
                aggregated[order.order_id].details.append(
                    OrderDetailMapper.to_model(unmapped.detail)
                )

        return aggregated.values()

    def _aggregator_from_unmapped_and_order(
        self, unmapped: UnmappedOrder
    ) -> OrderAggregator:
        order = OrderMapper.to_model(unmapped.order)
        detail = OrderDetailMapper.to_model(unmapped.detail)
        admin = (
            AdminMapper.to_model(unmapped.admin_user, unmapped.admin)
            if unmapped.admin and unmapped.admin_user
            else None
        )
        contractor = (
            ContractorMapper.to_model(
                unmapped.contractor_user, unmapped.contractor
            )
            if unmapped.contractor
            else None
        )
        return OrderAggregator(
            order=order, details=[detail], admin=admin, contractor=contractor
        )

    async def _execute_many(self, statement: Select) -> List[UnmappedOrder]:
        result = await self.executor.execute_many(statement)
        return [UnmappedOrder(row) for row in result]

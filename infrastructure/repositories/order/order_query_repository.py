from typing import List

from domain.dto.order.internal.order_filter_dto import OrderFilterDTO
from domain.entities.order.order import Order
from domain.repositories.order.order_query_repository import (
    OrderQueryRepository,
)
from infrastructure.database.mappers import OrderMapper
from infrastructure.repositories.base import QueryExecutor
from infrastructure.repositories.order.base import OrderQueryBuilder


class OrderQueryRepositoryImpl(OrderQueryRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def get_order(self, order_id: int) -> Order | None:
        stmt = self._get_query_buider().where_order_id(order_id).build()

        order = await self.executor.execute_scalar_one(stmt)
        if not order:
            return None
        return OrderMapper.to_model(order)

    async def get_order_for_detail(self, detail_id: int) -> Order | None:
        stmt = self._get_query_buider().where_detail_id(detail_id).build()

        order = await self.executor.execute_scalar_one(stmt)
        if not order:
            return None
        return OrderMapper.to_model(order)

    async def filter_orders(self, query: OrderFilterDTO) -> List[Order]:
        stmt = self._get_query_buider().apply_order_filter(query).build()

        orders = await self.executor.execute_scalar_many(stmt)
        return [OrderMapper.to_model(order) for order in orders]

    def _get_query_buider(self) -> OrderQueryBuilder:
        return OrderQueryBuilder()

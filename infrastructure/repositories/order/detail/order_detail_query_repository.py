from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.future import select

from domain.entities.order.detail import OrderDetail
from domain.repositories.order.detail.order_detail_query_repository import (
    OrderDetailQueryRepository,
)
from infrastructure.database.mappers import OrderDetailMapper
from infrastructure.database.models import OrderDetailBase
from infrastructure.repositories.base import QueryExecutor


class OrderDetailQueryRepositoryImpl(OrderDetailQueryRepository):
    def __init__(self, query_executor: QueryExecutor):
        self.query_executor = query_executor

    async def get_detail(self, detail_id: int) -> OrderDetail | None:
        query = select(OrderDetailBase).where(
            OrderDetailBase.detail_id == detail_id
        )
        detail = await self.query_executor.execute_scalar_one(query)
        if not detail:
            return None
        return OrderDetailMapper.to_model(detail)

    async def get_details_by_order_id(
        self, order_id: int
    ) -> List[OrderDetail]:
        query = select(OrderDetailBase).where(
            OrderDetailBase.order_id == order_id
        )
        results = await self.query_executor.execute_scalar_many(query)
        return [OrderDetailMapper.to_model(detail) for detail in results]

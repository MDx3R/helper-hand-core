from typing import List

from domain.entities.order.detail import OrderDetail
from domain.repositories.order.detail.order_detail_command_repository import (
    OrderDetailCommandRepository,
)
from infrastructure.database.mappers import OrderDetailMapper
from infrastructure.repositories.base import QueryExecutor
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import update
from infrastructure.database.models import OrderDetailBase


class OrderDetailCommandRepositoryImpl(OrderDetailCommandRepository):
    def __init__(self, query_executor: QueryExecutor):
        self.query_executor = query_executor

    async def update_detail(self, detail: OrderDetail) -> OrderDetail:
        query = (
            update(OrderDetailBase)
            .where(OrderDetailBase.detail_id == detail.detail_id)
            .values(detail.get_fields())
        )
        await self.query_executor.execute(query)
        return detail

    async def create_detail(self, detail: OrderDetail) -> OrderDetail:
        base = OrderDetailMapper.to_base(detail)
        await self.query_executor.add(base)
        return OrderDetailMapper.to_model(base)

    async def create_details(
        self, details: List[OrderDetail]
    ) -> List[OrderDetail]:
        query = (
            insert(OrderDetailBase)
            .values(
                [
                    {
                        k: v
                        for k, v in detail.get_fields().items()
                        if k != "detail_id"
                    }
                    for detail in details
                ]
            )
            .returning(OrderDetailBase)
        )
        results = await self.query_executor.execute_scalar_many(query)
        return [OrderDetailMapper.to_model(base) for base in results]

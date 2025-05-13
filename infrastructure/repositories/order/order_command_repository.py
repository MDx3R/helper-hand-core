from domain.dto.order.internal.user_command_dto import (
    SetOrderAdminDTO,
    SetOrderStatusDTO,
)
from domain.entities.order.order import Order
from domain.repositories.order.order_command_repository import (
    OrderCommandRepository,
)
from sqlalchemy import update
from infrastructure.database.models import OrderBase
from infrastructure.database.mappers import OrderMapper
from infrastructure.repositories.base import QueryExecutor


class OrderCommandRepositoryImpl(OrderCommandRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def create_order(self, order: Order) -> Order:
        base = OrderMapper.to_base(order)
        await self.executor.add(base)
        return OrderMapper.to_model(base)

    async def update_order(self, order: Order) -> Order:
        stmt = (
            update(OrderBase)
            .where(OrderBase.order_id == order.order_id)
            .values(order.get_fields())
        )
        await self.executor.execute(stmt)
        return order

    async def set_order_status(self, query: SetOrderStatusDTO) -> Order:
        stmt = (
            update(OrderBase)
            .where(OrderBase.order_id == query.order_id)
            .values(status=query.status)
            .returning(OrderBase)
        )
        order = await self.executor.execute_scalar_one(stmt)
        return OrderMapper.to_model(order)

    async def set_order_admin(self, query: SetOrderAdminDTO) -> Order:
        stmt = (
            update(OrderBase)
            .where(OrderBase.order_id == query.order_id)
            .values(admin_id=query.admin_id)
            .returning(OrderBase)
        )
        order = await self.executor.execute_scalar_one(stmt)
        return OrderMapper.to_model(order)

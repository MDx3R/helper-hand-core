from typing import List, Tuple
from sqlalchemy import func, select

from domain.entities import OrderDetail
from domain.repositories import OrderDetailRepository

from infrastructure.database.models import OrderDetailBase, ReplyBase
from infrastructure.database.mappers import OrderDetailMapper
from infrastructure.repositories.base import SQLAlchemyRepository

class SQLAlchemyOrderDetailRepository(OrderDetailRepository, SQLAlchemyRepository):
    async def get_detail_by_id(self, detail_id: int) -> OrderDetail | None:
        statement = select(OrderDetailBase).where(OrderDetailBase.detail_id == detail_id)
        detail = await self._execute_scalar_one(statement)
        return OrderDetailMapper.to_model(detail)

    async def save_detail(self, detail: OrderDetail) -> OrderDetail:
        if not detail.detail_id:
            detail_base = await self._insert_detail(detail)
        else:
            detail_base = await self._merge_detail(detail)
        return OrderDetailMapper.to_model(detail_base)

    async def save_details(self, details: List[OrderDetail]) -> List[OrderDetail]:
        return [await self.save_detail(detail) for detail in details]

    async def create_details(self, details: List[OrderDetail]) -> List[OrderDetail]:
        details = self._insert_details(details)
        return [OrderDetailMapper.to_model(detail) for detail in details]

    async def get_available_details_by_order_id(self, order_id: int) -> List[OrderDetail]:
        statement = (
            select(OrderDetailBase)
            .join(ReplyBase, OrderDetailBase.detail_id == ReplyBase.detail_id)
            .where(OrderDetailBase.order_id == order_id)
            .group_by(OrderDetailBase.detail_id, OrderDetailBase.count)
            .having(func.count(ReplyBase.detail_id) < OrderDetailBase.count)
        )

        details = await self._execute_scalar_many(statement)
        return [OrderDetailMapper.to_model(detail) for detail in details]

    async def _insert_detail(self, detail: OrderDetail) -> OrderDetailBase:
        async with self.transaction_manager.get_session() as session:
            detail_base = OrderDetailMapper.to_base(detail)
            session.add(detail_base)
            await session.flush()
            return detail_base
        
    async def _insert_details(self, details: List[OrderDetail]) -> OrderDetailBase:
        async with self.transaction_manager.get_session() as session:
            detail_bases = [OrderDetailMapper.to_base(detail) for detail in details]
            session.add_all(detail_bases)
            await session.flush()
            return detail_bases

    async def _merge_detail(self, detail: OrderDetail) -> OrderDetailBase:
        async with self.transaction_manager.get_session() as session:
            merged_detail: OrderDetailBase = await session.merge(OrderDetailMapper.to_base(detail))
            await session.flush()
            return merged_detail
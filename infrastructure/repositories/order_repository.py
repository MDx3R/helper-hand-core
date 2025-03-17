from typing import List, TypeVar, Type, Tuple
from sqlalchemy import select, update, exists, and_, Select, Sequence
from sqlalchemy.engine import Result, Row

from domain.repositories import OrderRepository
from domain.models import Order, DetailedOrder, Contractor
from domain.models.enums import OrderStatusEnum
from domain.exceptions import ApplicationException

from application.transactions import TransactionManager

from infrastructure.database.models import (
    Base, 
    UserBase,
    ContractorBase,
    OrderBase,
    OrderDetailBase,
    ReplyBase
)
from infrastructure.database.mappers import OrderMapper, DetailedOrderMapper, ContractorMapper

from infrastructure.repositories.base import SQLAlchemyRepository

O = TypeVar("O", bound=object)

class SQLAlchemyOrderRepository(OrderRepository, SQLAlchemyRepository):
    async def get_order_by_id(self, order_id: int) -> Order | None:
        statement = select(OrderBase).where(OrderBase.order_id == order_id)

        order = await self._execute_scalar_one(statement)
        return OrderMapper.to_model(order)
    
    async def get_order_by_detail_id(self, detail_id: int) -> Order | None:
        statement = select(OrderBase).join(
            OrderDetailBase, and_(OrderBase.order_id == OrderDetailBase.order_id, OrderDetailBase.detail_id == detail_id)
        )

        order = await self._execute_scalar_one(statement)
        return OrderMapper.to_model(order)
    
    async def get_order_by_id_and_contractor_id(self, order_id: int, contractor_id: int) -> Order | None:
        statement = select(OrderBase).where(
            and_(OrderBase.order_id == order_id, OrderBase.contractor_id == contractor_id)
        )

        order = await self._execute_scalar_one(statement)
        return OrderMapper.to_model(order)
    
    async def get_detailed_order_by_id(self, order_id: int) -> DetailedOrder | None:
        statement = select(OrderBase, OrderDetailBase).join(
            OrderDetailBase, and_(OrderBase.order_id == OrderDetailBase.order_id, OrderBase.order_id == order_id)
        )

        order, details = await self._execute_detailed_order_one(statement)    
        return DetailedOrderMapper.to_model(order, details)

    async def get_detailed_order_by_id_and_contractor_id(self, order_id: int, contractor_id: int) -> DetailedOrder | None:
        statement = select(OrderBase, OrderDetailBase).join(
            OrderDetailBase, 
            and_(
                OrderBase.order_id == OrderDetailBase.order_id, 
                OrderBase.order_id == order_id,
                OrderBase.contractor_id == contractor_id
            )
        )

        order, details = await self._execute_detailed_order_one(statement)
        return DetailedOrderMapper.to_model(order, details)

    async def get_detailed_open_orders_by_page(self, page: int = 1, size: int = None) -> List[DetailedOrder]:
        offset = self._calculate_offset(page, size)
        statement = select(OrderBase, OrderDetailBase).join(
            OrderDetailBase, OrderBase.order_id == OrderDetailBase.order_id
        ).where(OrderBase.status == OrderStatusEnum.open).offset(offset).limit(size)
        
        orders = await self._execute_detailed_order_many(statement)
        return self._map_many_order_and_details_bases_to_detailed_orders(orders)

    async def get_detailed_open_orders_by_last_order_id(self, last_order_id: int = None, size: int = None) -> List[DetailedOrder]:
        statement = select(OrderBase, OrderDetailBase).join(
            OrderDetailBase, OrderBase.order_id == OrderDetailBase.order_id
        ).where(OrderBase.status == OrderStatusEnum.open)
        
        if last_order_id:
            statement = statement.where(OrderBase.order_id > last_order_id)
        
        statement = statement.limit(size)
        
        orders = await self._execute_detailed_order_many(statement)
        return self._map_many_order_and_details_bases_to_detailed_orders(orders)

    async def get_contractor_by_order_id(self, order_id: int) -> Contractor | None:
        statement = (
            select(UserBase, ContractorBase)
            .join(
                UserBase, 
                UserBase.user_id == ContractorBase.contractor_id
            )
            .join(
                Order, 
                and_(Order.contractor_id == ContractorBase.contractor_id, Order.order_id == order_id)
            )
        )
        row = await self._execute_one(statement)
        if not row:
            return None
        
        user, contractor = row
        return ContractorMapper.to_model(user, contractor)

    async def get_contractor_orders_by_page(self, contractor_id: int, page: int = 1, size: int = None) -> List[Order]:
        offset = self._calculate_offset(page, size)
        statement = select(OrderBase).where(OrderBase.contractor_id == contractor_id).offset(offset).limit(size)
        
        orders = await self._execute_scalar_many(statement)
        return self._map_many_order_bases_to_orders(orders)

    async def get_contractor_orders_by_last_order_id(self, contractor_id: int, last_order_id: int = None, size: int = None) -> List[Order]:
        statement = select(OrderBase).where(OrderBase.contractor_id == contractor_id)
        if last_order_id:
            statement = statement.where(OrderBase.order_id > last_order_id)
        statement = statement.limit(size)
        
        orders = await self._execute_scalar_many(statement)
        return self._map_many_order_bases_to_orders(orders)

    async def get_contractor_detailed_orders_by_page(self, contractor_id: int, page: int = 1, size: int = None) -> List[DetailedOrder]:
        offset = self._calculate_offset(page, size)
        statement = select(OrderBase, OrderDetailBase).join(
            OrderDetailBase, OrderBase.order_id == OrderDetailBase.order_id
        ).where(OrderBase.contractor_id == contractor_id).offset(offset).limit(size)
        
        orders = await self._execute_detailed_order_many(statement)
        return self._map_many_order_and_details_bases_to_detailed_orders(orders)

    async def get_contractor_detailed_orders_by_last_order_id(self, contractor_id: int, last_order_id: int = None, size: int = None) -> List[DetailedOrder]:
        statement = select(OrderBase, OrderDetailBase).join(
            OrderDetailBase, OrderBase.order_id == OrderDetailBase.order_id
        ).where(OrderBase.contractor_id == contractor_id)
        if last_order_id:
            statement = statement.where(OrderBase.order_id > last_order_id)
        statement = statement.limit(size)
        
        orders = await self._execute_detailed_order_many(statement)
        return self._map_many_order_and_details_bases_to_detailed_orders(orders)

    async def get_admin_orders_by_page(self, admin_id: int, page: int = 1, size: int = None) -> List[Order]:
        offset = self._calculate_offset(page, size)
        statement = select(OrderBase).where(OrderBase.admin_id == admin_id).offset(offset).limit(size)
        
        orders = await self._execute_scalar_many(statement)
        return self._map_many_order_bases_to_orders(orders)

    async def get_admin_orders_by_last_order_id(self, admin_id: int, last_order_id: int = None, size: int = None) -> List[Order]:
        statement = select(OrderBase).where(OrderBase.admin_id == admin_id)
        if last_order_id:
            statement = statement.where(OrderBase.order_id > last_order_id)
        statement = statement.limit(size)
        
        orders = await self._execute_scalar_many(statement)
        return self._map_many_order_bases_to_orders(orders)

    async def get_contractee_orders_by_page(self, contractee_id: int, page: int = 1, size: int = None) -> List[Order]:
        offset = self._calculate_offset(page, size)
        statement = select(OrderBase)\
            .join(OrderDetailBase, OrderBase.order_id == OrderDetailBase.order_id)\
            .join(ReplyBase, OrderDetailBase.detail_id == ReplyBase.detail_id)\
            .where(ReplyBase.contractee_id == contractee_id).offset(offset).limit(size)

        orders = await self._execute_scalar_many(statement)
        return self._map_many_order_bases_to_orders(orders)

    async def get_contractee_orders_by_last_order_id(self, contractee_id: int, last_order_id: int = None, size: int = None) -> List[Order]:
        statement = select(OrderBase)\
            .join(OrderDetailBase, OrderBase.order_id == OrderDetailBase.order_id)\
            .join(ReplyBase, OrderDetailBase.detail_id == ReplyBase.detail_id)\
            .where(ReplyBase.contractee_id == contractee_id)
        if last_order_id:
            statement = statement.where(OrderBase.order_id > last_order_id)
        statement = statement.limit(size)
        
        orders = await self._execute_scalar_many(statement)
        return self._map_many_order_bases_to_orders(orders)

    async def get_orders_by_page(self, page: int = 1, size: int = None) -> List[Order]:
        offset = self._calculate_offset(page, size)
        statement = select(OrderBase).offset(offset).limit(size)
        
        orders = await self._execute_scalar_many(statement)
        return self._map_many_order_bases_to_orders(orders)

    async def get_detailed_orders_by_page(self, page: int = 1, size: int = None) -> List[DetailedOrder]:
        offset = self._calculate_offset(page, size)
        statement = select(OrderBase, OrderDetailBase).join(
            OrderDetailBase, OrderBase.order_id == OrderDetailBase.order_id
        ).offset(offset).limit(size)
        
        orders = await self._execute_detailed_order_many(statement)
        return self._map_many_order_and_details_bases_to_detailed_orders(orders)

    async def get_open_orders_by_page(self, page: int = 1, size: int = None) -> List[Order]:
        offset = self._calculate_offset(page, size)
        statement = select(OrderBase, OrderDetailBase).join(
            OrderDetailBase, OrderBase.order_id == OrderDetailBase.order_id
        ).where(OrderBase.status == OrderStatusEnum.open).offset(offset).limit(size)
        
        orders = await self._execute_scalar_many(statement)
        return self._map_many_order_bases_to_orders(orders)

    async def get_closed_orders_by_page(self, page: int = 1, size: int = None) -> List[Order]:
        offset = self._calculate_offset(page, size)
        statement = select(OrderBase, OrderDetailBase).join(
            OrderDetailBase, OrderBase.order_id == OrderDetailBase.order_id
        ).where(OrderBase.status == OrderStatusEnum.closed).offset(offset).limit(size)
        
        orders = await self._execute_scalar_many(statement)
        return self._map_many_order_bases_to_orders(orders)

    async def get_active_orders_by_page(self, page: int = 1, size: int = None) -> List[DetailedOrder]:
        offset = self._calculate_offset(page, size)
        statement = select(OrderBase, OrderDetailBase).join(
            OrderDetailBase, OrderBase.order_id == OrderDetailBase.order_id
        ).where(OrderBase.status == OrderStatusEnum.active).offset(offset).limit(size)
        
        orders = await self._execute_scalar_many(statement)
        return self._map_many_order_bases_to_orders(orders)

    async def get_detailed_unassigned_orders_by_page(self, page: int = 1, size: int = None) -> List[DetailedOrder]:
        offset = self._calculate_offset(page, size)
        statement = select(OrderBase, OrderDetailBase).join(
            OrderDetailBase, OrderBase.order_id == OrderDetailBase.order_id
        ).where(OrderBase.admin_id == None).offset(offset).limit(size)

        orders = await self._execute_detailed_order_many(statement)
        return self._map_many_order_and_details_bases_to_detailed_orders(orders)

    async def get_detailed_unassigned_orders_by_last_order_id(self, last_order_id: int = None, size: int = None) -> List[DetailedOrder]:
        statement = select(OrderBase, OrderDetailBase).join(
            OrderDetailBase, OrderBase.order_id == OrderDetailBase.order_id
        ).where(OrderBase.admin_id == None)
        
        if last_order_id:
            statement = statement.where(OrderBase.order_id > last_order_id)
        
        statement = statement.limit(size)
        
        orders = await self._execute_detailed_order_many(statement)
        return self._map_many_order_and_details_bases_to_detailed_orders(orders)
    
    async def _execute_detailed_order_one(self, statement: Select[Tuple[OrderBase, OrderDetailBase]]) -> Tuple[OrderBase, List[OrderDetailBase]] | Tuple[None,  List]:
        rows = await self._execute_many(statement)
        
        if not rows:
            return None, []

        details = []
        for order, detail in rows:
            details.append(detail)

        return order, details

    async def _execute_detailed_order_many(self, statement: Select[Tuple[OrderBase, OrderDetailBase]]) -> List[Tuple[OrderBase, List[OrderDetailBase]]]:
        rows = (await self._execute(statement)).all()
        if not rows:
            return []

        orders = self._parse_order_details_join(rows)
        return orders

    def _parse_order_details_join(self, rows: Sequence[Row[Tuple[OrderBase, OrderDetailBase]]]) -> List[Tuple[OrderBase, List[OrderDetailBase]]]:
        orders = {}
        for order, detail in rows:
            if order.order_id not in orders:
                orders[order.order_id] = (order, [])
            orders[order.order_id][1].append(detail)

        return orders.values()

    async def save_order(self, order: Order) -> Order:
        if not order.order_id:
            order_base = await self._insert_order(order)
        else:
            order_base = await self._merge_order(order)

        return OrderMapper.to_model(order_base)

    async def _insert_order(self, order: Order) -> OrderBase:
        async with self.transaction_manager.get_session() as session:
            order_base = OrderMapper.to_base(order)
            session.add(order_base)
            await session.flush()
            
            return order_base
        
    async def _merge_order(self, order: Order) -> OrderBase:
        async with self.transaction_manager.get_session() as session:
            merged_order: OrderBase = await session.merge(OrderMapper.to_base(order))
            await session.flush()

            return merged_order
    
    async def change_order_status(self, order_id: int, status: OrderStatusEnum) -> Order:
        statement = update(OrderBase).where(
            OrderBase.order_id == order_id
        ).values(status=status).returning(OrderBase)
        
        order = (await self._execute(statement)).fetchone()
        return OrderMapper.to_model(order)
    
    def _map_many_order_bases_to_orders(self, orders: List[OrderBase]) -> List[Order]:
        return [OrderMapper.to_model(order) for order in orders]

    def _map_many_order_and_details_bases_to_detailed_orders(self, orders: List[Tuple[OrderBase, List[OrderDetailBase]]]) -> List[DetailedOrder]:
        return [DetailedOrderMapper.to_model(order, details) for order, details in orders]
from typing import List

from .order_dto import OrderOutputDTO
from .order_detail_dto import OrderDetailOutputDTO

from domain.entities import Order, OrderDetail, DetailedOrder

class DetailedOrderOutputDTO(OrderOutputDTO):
    """
    Расширенный `OrderOutputDTO` для данных заказа вместе со сведениями о нем.

    Этот класс используется для представления данных заказа вместе со сведениями о нем на уровень представления.
    """

    details: List[OrderDetailOutputDTO]

    @classmethod
    def from_order(cls, order: DetailedOrder) -> 'DetailedOrderOutputDTO':
        """
        Преобразует `DetailedOrder` в `DetailedOrderOutputDTO`.
        """
        return cls(
            order_id=order.order_id,
            contractor_id=order.contractor_id,
            about=order.about,
            address=order.address,
            status=order.status,
            admin_id=order.admin_id,
            details=order.details
        )

    @classmethod
    def from_order_and_details(cls, order: Order, details: List[OrderDetail]) -> 'DetailedOrderOutputDTO':
        """
        Преобразует `Order` и `OrderDetail` в `DetailedOrderOutputDTO`.
        """
        return cls(
            order_id=order.order_id,
            contractor_id=order.contractor_id,
            about=order.about,
            address=order.address,
            status=order.status,
            admin_id=order.admin_id,
            details=[OrderDetailOutputDTO.from_order_detail(det) for det in details]
        )
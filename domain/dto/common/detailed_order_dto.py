from typing import List

from .order_dto import OrderDTO
from .order_detail_dto import OrderDetailDTO

from domain.entities import Order, OrderDetail, DetailedOrder

class DetailedOrderDTO(OrderDTO):
    """
    Расширенный `OrderDTO` для данных заказа вместе со сведениями о нем.
    """

    details: List[OrderDetailDTO]

    @classmethod
    def from_order(cls, order: DetailedOrder) -> 'DetailedOrderDTO':
        return cls.from_model(order)

    @classmethod
    def from_order_and_details(cls, order: Order, details: List[OrderDetail]) -> 'DetailedOrderDTO':
        return cls.from_order(
            DetailedOrder.model_validate(
                order.get_fields() | {"details": details}
            )
        )
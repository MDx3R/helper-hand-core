from typing import Optional
from pydantic import BaseModel

from domain.models import Order 
from domain.models.enums import OrderStatusEnum

class OrderOutputDTO(BaseModel):
    """
    DTO выходных данных заказа.

    Этот класс используется для представления данных заказа на уровень представления.
    """

    order_id: int
    contractor_id: int
    about: str
    address: str
    status: OrderStatusEnum
    admin_id: Optional[int]

    @classmethod
    def from_order(cls, order: Order) -> 'OrderOutputDTO':
        """
        Преобразует `Order` в `OrderOutputDTO`.
        """
        return cls(
            order_id=order.order_id,
            contractor_id=order.contractor_id,
            about=order.about,
            address=order.address,
            status=order.status,
            admin_id=order.admin_id
        )
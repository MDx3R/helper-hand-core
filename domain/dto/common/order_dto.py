from typing import Optional
from pydantic import BaseModel

from domain.entities import Order 
from domain.entities.enums import OrderStatusEnum
from domain.dto.base import ApplicationDTO

class OrderDTO(ApplicationDTO):
    order_id: int
    contractor_id: int
    about: str
    address: str
    status: OrderStatusEnum
    admin_id: Optional[int]

    @classmethod
    def from_order(cls, order: Order) -> 'OrderDTO':
        return cls.from_model(order)
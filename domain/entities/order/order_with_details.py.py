from typing import List

from domain.entities.base import ApplicationModel

from .detail import OrderDetail
from .order import Order


class OrderWithDetails(ApplicationModel):
    """
    Композитная модель заказа и его сведений.
    """

    order: Order
    details: List[OrderDetail]

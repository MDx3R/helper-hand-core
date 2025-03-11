from typing import List

from .order import Order
from .order_detail import OrderDetail

class DetailedOrder(Order):
    """
    Расширенная модель заказа.

    Представляет данные заказа, включая описание, адрес, идентификаторы заказчика и администратора, привязанного к заказу, 
    статус заказа, а также сведения о заказе.
    """

    details: List[OrderDetail]
    """Сведения о заказе."""
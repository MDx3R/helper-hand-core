from typing import Optional
from .base import ApplicationModel

from .enums import OrderStatusEnum

class Order(ApplicationModel):
    """
    Модель заказа.

    Представляет данные заказа, включая описание, адрес, идентификаторы заказчика и администратора, привязанного к заказу,
    а также статус заказа.
    """

    order_id: Optional[int] = None
    """Уникальный идентификатор заказа. Может быть `None` при создании нового заказа."""

    contractor_id: int
    """Идентификатор владельца заказа (заказчика)."""
    
    about: str
    """Описание заказа."""
    
    address: str
    """Адрес заказа."""

    status: OrderStatusEnum = OrderStatusEnum.created
    """Статус заказа. По умолчанию `OrderStatusEnum.created`."""

    admin_id: Optional[int] = None
    """Идентификатор администратора, привязанного к заказу. Может отсутствовать"""

    @property
    def literal_status(self) -> str:
        """
        Возвращает строковое представление статуса заказа на русском языке.
        """
        match self.status:
            case OrderStatusEnum.created:
                return "Открытый"
            case OrderStatusEnum.open:
                return "Открытый"
            case OrderStatusEnum.closed:
                return "Закрытый"
            case OrderStatusEnum.active:
                return "Активный"
            case OrderStatusEnum.fulfilled:
                return "Завершенный"
            case _:
                return "Отмененный"
            
    def is_owner(self, contractor_id: int) -> bool:
        return contractor_id == self.contractor_id
    
    def is_supervisor(self, admin_id: int) -> bool:
        return admin_id == self.admin_id
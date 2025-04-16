from typing import Optional

from domain.entities.base import ApplicationModel

from .enums import OrderStatusEnum


class Order(ApplicationModel):
    """
    Модель заказа.
    """

    order_id: Optional[int] = None
    """Уникальный идентификатор заказа. Может быть `None` при создании нового заказа."""

    contractor_id: int
    about: str
    address: str
    status: OrderStatusEnum = OrderStatusEnum.created

    admin_id: Optional[int] = None
    """Идентификатор администратора, курирующего заказ."""

    @property
    def supervisor_id(self) -> Optional[int]:
        """Свойство для получения идентификатора куратора заказа."""
        return self.admin_id

from domain.exceptions.base import ServiceException
from typing import Optional

class MissingOrderDetailsException(ServiceException):
    """Вызывается при попытке создать заказ без сведений о заказе."""
    def __init__(self, message: str = "Сведения заказа отсутствуют"):
        super().__init__(message)

class OrderStatusChangeNotAllowedException(ServiceException):
    """Вызывается при попытке изменить статус заказа в конкретном состоянии на недопустимый."""
    def __init__(self, order_id: int, status: str, comment: str | None = None):
        self.order_id = order_id
        self.status = status
        self.comment = comment

        message = f"Невозможно изменить статус заказа (id={order_id}) на '{status}'"
        if comment:
            message += f": {comment}"

        super().__init__(message)

class OrderActionNotAllowedException(ServiceException):
    """Вызывается, когда действие недоступно из-за текущего статуса заказа."""
    def __init__(self, order_id: int, status: str, action: str):
        self.order_id = order_id
        self.status = status
        self.action = action

        message = f"Невозможно выполнить действие '{action}' для заказа (id={order_id}) со статусом '{status}'"
        super().__init__(message)


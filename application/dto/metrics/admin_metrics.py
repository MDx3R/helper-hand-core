from decimal import Decimal

from domain.dto.base import ApplicationDTO


class AdminMetrics(ApplicationDTO):
    orders: int
    open_orders: int
    completed_orders: int
    amount: Decimal
    hours_worked: float

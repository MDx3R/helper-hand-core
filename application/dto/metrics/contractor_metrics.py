from decimal import Decimal

from domain.dto.base import ApplicationDTO


class ContractorMetrics(ApplicationDTO):
    orders: int
    open_orders: int
    active_orders: int
    completed_orders: int
    replies: int
    pending_replies: int
    spent: Decimal
    hours_worked: float

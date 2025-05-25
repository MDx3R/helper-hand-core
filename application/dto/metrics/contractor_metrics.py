from decimal import Decimal

from domain.dto.base import ApplicationDTO


class ContractorMetrics(ApplicationDTO):
    orders: int
    completed_orders: int
    replies: int
    spent: Decimal
    hours_worked: float

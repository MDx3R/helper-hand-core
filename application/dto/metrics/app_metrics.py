from decimal import Decimal

from domain.dto.base import ApplicationDTO


class AppMetrics(ApplicationDTO):
    users: int
    orders: int
    replies: int
    total_amount: Decimal
    average_wager: Decimal

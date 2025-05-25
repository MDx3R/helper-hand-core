from decimal import Decimal

from domain.dto.base import ApplicationDTO


class ContracteeMetrics(ApplicationDTO):
    replies: int
    accepted_replies: int
    orders_with_accepted_replies: int
    earned: Decimal
    hours_worked: float
    average_wager: Decimal

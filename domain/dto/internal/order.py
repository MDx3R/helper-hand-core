from typing import List, Optional

from domain.dto.input import OrderDetailInputDTO, OrderInputDTO
from domain.entities.enums import OrderStatusEnum

from .base import ContextDTO, OrderIdDTO, PaginationDTO, UserIdDTO


class CreateOrderDTO(ContextDTO):
    order_input: OrderInputDTO
    details_input: List[OrderDetailInputDTO]


class GetOrderDTO(OrderIdDTO):
    pass


class OrderManagementDTO(OrderIdDTO, ContextDTO):
    pass


class SetOrderActiveDTO(OrderManagementDTO):
    pass


class TakeOrderDTO(OrderManagementDTO):
    pass


class ApproveOrderDTO(OrderManagementDTO):
    pass


class DisapproveOrderDTO(OrderManagementDTO):
    pass


class CancelOrderDTO(OrderManagementDTO):
    pass


class CloseOrderDTO(OrderManagementDTO):
    pass


class OpenOrderDTO(OrderManagementDTO):
    pass


class FulfillOrderDTO(OrderManagementDTO):
    pass


class GetUserOrdersDTO(UserIdDTO, PaginationDTO):
    pass


class GetUserOrdersWithStatusDTO(GetUserOrdersDTO):
    status: Optional[OrderStatusEnum] = None

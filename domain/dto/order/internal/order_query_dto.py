from typing import Optional
from domain.dto.base import LastObjectDTO, PaginationDTO
from domain.dto.order.internal.base import OrderIdDTO
from domain.dto.user.internal.base import UserIdDTO
from domain.entities.order.enums import OrderStatusEnum


class GetOrderDTO(OrderIdDTO):
    pass


class GetUserOrderDTO(OrderIdDTO, UserIdDTO):
    pass


class GetUserOrdersDTO(UserIdDTO, PaginationDTO):
    pass


class GetUserOrderAfterDTO(UserIdDTO, LastObjectDTO):
    pass


class GetUserOrdersWithStatusDTO(GetUserOrdersDTO):
    status: Optional[OrderStatusEnum] = None

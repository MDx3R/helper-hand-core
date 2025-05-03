from typing import Optional
from domain.dto.base import LastObjectDTO, PaginationDTO
from domain.dto.order.internal.base import OrderIdDTO
from domain.dto.user.internal.base import UserIdDTO
from domain.dto.user.internal.user_context_dto import WithUserContextDTO
from domain.entities.order.enums import OrderStatusEnum


class GetOrderDTO(OrderIdDTO, WithUserContextDTO):
    pass


class GetUserOrderDTO(OrderIdDTO, UserIdDTO):
    pass


class GetUserOrdersDTO(UserIdDTO, PaginationDTO):
    pass


class GetUserOrderAfterDTO(UserIdDTO, LastObjectDTO):
    pass


class GetOrderAfterDTO(LastObjectDTO, WithUserContextDTO):
    pass


class GetUserOrdersWithStatusDTO(GetUserOrdersDTO):
    status: Optional[OrderStatusEnum] = None

from domain.dto.base import InternalDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO


class OrderIdDTO(InternalDTO):
    order_id: int


class OrderWithUserContextDTO(InternalDTO):
    context: UserContextDTO

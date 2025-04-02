from typing import Optional

from domain.dto.base import ApplicationDTO
from domain.dto.context import UserContextDTO

class InternalDTO(ApplicationDTO):
    pass

class UserIdDTO(InternalDTO):
    user_id: int

class OrderIdDTO(InternalDTO):
    order_id: int

class LastObjectDTO(InternalDTO):
    last_id: Optional[int] = None

class PaginationDTO(InternalDTO):
    page: int = 1
    size: int = 15

class ContextDTO(InternalDTO):
    "Следует использовать только для создания производных DTO."
    context: UserContextDTO
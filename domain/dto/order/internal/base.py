from typing import Optional
from domain.dto.base import InternalDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO


class OrderIdDTO(InternalDTO):
    order_id: int


class DetailIdDTO(InternalDTO):
    detail_id: int


class OrderSignatureDTO(InternalDTO):
    order_id: int
    contractor_id: Optional[int] = None
    admin_id: Optional[int] = None


class OrderWithUserContextDTO(InternalDTO):
    context: UserContextDTO

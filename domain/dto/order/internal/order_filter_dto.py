from typing import Optional
from domain.dto.base import InternalDTO, PaginationDTO
from domain.entities.order.enums import OrderStatusEnum


class OrderFilterDTO(PaginationDTO):
    status: Optional[OrderStatusEnum] = None
    contractor_id: Optional[int] = None
    admin_id: Optional[int] = None
    contractee_id: Optional[int] = None

    @property
    def supervisor_id(self) -> int:
        return self.admin_id


class DetailFilterDTO(PaginationDTO):
    order_id: Optional[int] = None
    detail_id: Optional[int] = None

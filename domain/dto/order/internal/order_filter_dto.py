from typing import Literal, Optional
from domain.dto.base import InternalDTO, PaginationDTO, SortingDTO
from domain.entities.order.enums import OrderStatusEnum


class OrderFilterDTO(PaginationDTO, SortingDTO):
    order_id: Optional[int] = None
    status: Optional[OrderStatusEnum] = None
    contractor_id: Optional[int] = None
    admin_id: Optional[int] = None
    contractee_id: Optional[int] = None
    only_available_details: bool = False

    @property
    def supervisor_id(self) -> int:
        return self.admin_id


class DetailFilterDTO(PaginationDTO):
    order_id: Optional[int] = None
    detail_id: Optional[int] = None

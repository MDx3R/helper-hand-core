from typing import Optional

from pydantic import Field
from domain.dto.base import PaginationDTO, SortingDTO
from domain.entities.order.enums import OrderStatusEnum


class OrderFilterDTO(PaginationDTO, SortingDTO):
    # TODO: Nullable вместо default=-1
    order_id: Optional[int] = None
    status: Optional[OrderStatusEnum] = None
    contractor_id: Optional[int] = None
    admin_id: Optional[int] = Field(default=-1)
    contractee_id: Optional[int] = None
    only_available_details: bool = False

    @property
    def supervisor_id(self) -> Optional[int]:
        return self.admin_id if self.admin_id_set else None

    @property
    def admin_id_set(self) -> bool:
        return self.admin_id != -1


class DetailFilterDTO(PaginationDTO):
    order_id: Optional[int] = None
    detail_id: Optional[int] = None

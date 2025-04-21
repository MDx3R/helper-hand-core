from typing import Optional
from domain.dto.base import InternalDTO, PaginationDTO
from domain.entities.order.enums import OrderStatusEnum


class OrderFilterDTO(PaginationDTO):
    status: Optional[OrderStatusEnum] = None
    contractor_id: Optional[int] = None
    admin_id: Optional[int] = None

    @property
    def supervisor_id(self) -> int:
        return self.admin_id


class ContracteeOrderFilterDTO(OrderFilterDTO):
    contractee_id: int

from typing import List, Optional
from domain.dto.base import InternalDTO, PaginationDTO
from domain.entities.enums import CitizenshipEnum, GenderEnum, PositionEnum
from domain.entities.user.enums import RoleEnum, UserStatusEnum


class UserFilterDTO(PaginationDTO):
    status: Optional[UserStatusEnum] = None
    phone_number: Optional[str] = None
    role: Optional[RoleEnum] = None


class AdminFilterDTO(UserFilterDTO):
    pass


class ContractorFilterDTO(UserFilterDTO):
    pass


class ContracteeFilterDTO(UserFilterDTO):
    gender: Optional[GenderEnum] = None
    citizenship: Optional[CitizenshipEnum] = None
    positions: Optional[List[PositionEnum]] = None

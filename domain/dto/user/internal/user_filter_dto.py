from typing import List, Optional
from domain.dto.base import InternalDTO, PaginationDTO
from domain.entities.enums import CitizenshipEnum, GenderEnum, PositionEnum
from domain.entities.user.enums import RoleEnum, UserStatusEnum


class UserBaseFilterDTO(InternalDTO, PaginationDTO):
    status: Optional[UserStatusEnum] = None


class UserFilterDTO(UserBaseFilterDTO):
    number: Optional[str] = None
    role: Optional[RoleEnum] = None


class AdminFilterDTO(UserBaseFilterDTO):
    pass


class ContractorFilterDTO(UserBaseFilterDTO):
    pass


class ContracteeFilterDTO(UserBaseFilterDTO):
    gender: Optional[GenderEnum] = None
    citizenship: Optional[CitizenshipEnum] = None
    positions: List[PositionEnum] = []

from domain.dto.base import ApplicationDTO, ContextDTO, PaginationDTO
from domain.dto.user.base import WithCredentialsDTO
from domain.entities.user.enums import RoleEnum, UserStatusEnum


class UserContextDTO(ContextDTO, WithCredentialsDTO):
    user_id: int
    role: RoleEnum
    status: UserStatusEnum


class WithUserContextDTO(ApplicationDTO):
    context: UserContextDTO


class PaginatedDTO(WithUserContextDTO, PaginationDTO):
    pass

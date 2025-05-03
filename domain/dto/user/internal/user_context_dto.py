from domain.dto.base import ApplicationDTO, ContextDTO
from domain.dto.user.base import TelegramCredentialsDTO
from domain.entities.user.enums import RoleEnum, UserStatusEnum


class UserContextDTO(ContextDTO, TelegramCredentialsDTO):
    user_id: int
    role: RoleEnum
    status: UserStatusEnum


class WithUserContextDTO(ApplicationDTO):
    context: UserContextDTO

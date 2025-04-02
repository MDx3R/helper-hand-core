from domain.dto.input.registration import UserResetDTO

from .base import (
    ContextDTO,
    OrderIdDTO,
    UserIdDTO,
    PaginationDTO
)

class ResetDTO(ContextDTO):
    user: UserResetDTO

class GetUserDTO(UserIdDTO):
    pass

class UserManagementDTO(UserIdDTO, ContextDTO):
    pass

class UserNotificationDTO(UserIdDTO, ContextDTO):
    message: str = ""
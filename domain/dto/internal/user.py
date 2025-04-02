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

class GetUserWithContextDTO(GetUserDTO, ContextDTO):
    pass

class UserManagementDTO(UserIdDTO, ContextDTO):
    pass

class ApproveUserDTO(UserIdDTO):
    pass

class DisapproveUserDTO(UserIdDTO):
    pass

class DropUserDTO(UserIdDTO):
    pass

class BanUserDTO(UserIdDTO):
    pass

class UserNotificationDTO(UserIdDTO, ContextDTO):
    message: str = ""
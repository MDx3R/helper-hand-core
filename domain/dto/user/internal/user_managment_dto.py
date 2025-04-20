from domain.dto.user.internal.base import UserIdDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO


class UserManagementDTO(UserIdDTO):
    context: UserContextDTO


class ApproveUserDTO(UserManagementDTO):
    pass


class DisapproveUserDTO(UserManagementDTO):
    pass


class DropUserDTO(UserManagementDTO):
    pass


class BanUserDTO(UserManagementDTO):
    pass

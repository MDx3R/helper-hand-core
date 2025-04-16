from domain.dto.user.internal.base import UserIdDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO


class UserManagementDTO(UserIdDTO):
    context: UserContextDTO


class ApproveUserDTO(UserIdDTO):
    pass


class DisapproveUserDTO(UserIdDTO):
    pass


class DropUserDTO(UserIdDTO):
    pass


class BanUserDTO(UserIdDTO):
    pass

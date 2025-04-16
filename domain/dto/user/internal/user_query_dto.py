from domain.dto.user.internal.base import UserIdDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO


class GetUserDTO(UserIdDTO):
    pass


class GetUserWithContextDTO(GetUserDTO):
    context: UserContextDTO

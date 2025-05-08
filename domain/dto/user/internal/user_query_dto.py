from domain.dto.user.internal.base import UserIdDTO
from domain.dto.user.internal.user_context_dto import (
    UserContextDTO,
    WithUserContextDTO,
)


class GetUserDTO(UserIdDTO, WithUserContextDTO):
    pass


# class GetUserWithContextDTO(GetUserDTO):
#     context: UserContextDTO

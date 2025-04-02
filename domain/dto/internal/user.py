from domain.dto.input.registration import UserResetDTO

from .base import (
    ContextDTO,
    GetOrderDTO,
    GetUserDTO,
    PaginationDTO
)

class ResetDTO(ContextDTO):
    user: UserResetDTO
from domain.dto.input.registration import UserResetDTO

from .base import (
    ContextDTO,
    OrderIdDTO,
    UserIdDTO,
    PaginationDTO
)

class ResetDTO(ContextDTO):
    user: UserResetDTO
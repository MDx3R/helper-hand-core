from typing import Optional
from domain.dto.user.request.user_input_dto import (
    UserInputDTO,
    WithCredentialsInputDTO,
)


class AdminInputDTO(UserInputDTO):
    about: str
    contractor_id: Optional[int] = None


class CreateAdminDTO(WithCredentialsInputDTO):
    user: AdminInputDTO

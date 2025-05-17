from typing import Optional
from domain.dto.user.request.create_user_dto import BaseCreateUserDTO
from domain.dto.user.request.user_input_dto import UserInputDTO


class AdminInputDTO(UserInputDTO):
    about: str
    contractor_id: Optional[int] = None


class CreateAdminDTO(BaseCreateUserDTO):
    user: AdminInputDTO

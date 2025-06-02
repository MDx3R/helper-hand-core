from typing import Optional
from domain.dto.user.internal.user_context_dto import WithUserContextDTO
from domain.dto.user.request.create_user_dto import BaseCreateUserDTO
from domain.dto.user.request.user_input_dto import UserInputDTO


class AdminInputDTO(UserInputDTO):
    about: str


class CreateAdminDTO(BaseCreateUserDTO):
    user: AdminInputDTO


class UpdateAdminDTO(WithUserContextDTO):
    user: AdminInputDTO

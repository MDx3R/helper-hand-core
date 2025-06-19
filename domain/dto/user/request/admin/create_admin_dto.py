from pydantic import Field
from domain.dto.user.internal.user_context_dto import WithUserContextDTO
from domain.dto.user.request.create_user_dto import BaseCreateUserDTO
from domain.dto.user.request.user_input_dto import UserInputDTO


class AdminInputDTO(UserInputDTO):
    about: str = Field(..., min_length=1, max_length=256)


class CreateAdminDTO(BaseCreateUserDTO):
    user: AdminInputDTO


class UpdateAdminDTO(WithUserContextDTO):
    user: AdminInputDTO

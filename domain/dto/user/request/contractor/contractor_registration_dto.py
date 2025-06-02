from domain.dto.user.internal.user_context_dto import WithUserContextDTO
from domain.dto.user.request.create_user_dto import BaseCreateUserDTO
from domain.dto.user.request.user_input_dto import (
    BaseRegisterUserDTO,
    UserInputDTO,
)


class ContractorInputDTO(UserInputDTO):
    about: str


class RegisterContractorDTO(BaseRegisterUserDTO):
    user: ContractorInputDTO


class ResetContractorDTO(WithUserContextDTO):
    user: ContractorInputDTO


class CreateContractorDTO(BaseCreateUserDTO):
    user: ContractorInputDTO


class UpdateContractorDTO(WithUserContextDTO):
    user: ContractorInputDTO

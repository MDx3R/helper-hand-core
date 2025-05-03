from domain.dto.user.internal.user_context_dto import WithUserContextDTO
from domain.dto.user.request.user_input_dto import (
    UserInputDTO,
    WithCredentialsInputDTO,
)


class ContractorInputDTO(UserInputDTO):
    about: str


class RegisterContractorDTO(WithCredentialsInputDTO):
    user: ContractorInputDTO


class ResetContractorDTO(WithUserContextDTO):
    user: ContractorInputDTO

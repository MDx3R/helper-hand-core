from domain.dto.input import ContracteeInputDTO
from domain.dto.user.request.user_registration_dto import (
    TelegramUserRegistrationDTO,
    UserRegistrationDTO,
    UserResetDTO,
    WebUserRegistrationDTO,
)


class ContracteeRegistrationDTO(ContracteeInputDTO, UserRegistrationDTO):
    pass


class ContracteeResetDTO(ContracteeRegistrationDTO, UserResetDTO):
    pass


class WebContracteeRegistrationDTO(
    WebUserRegistrationDTO, ContracteeRegistrationDTO
):
    pass


class TelegramContracteeRegistrationDTO(
    TelegramUserRegistrationDTO, ContracteeRegistrationDTO
):
    pass

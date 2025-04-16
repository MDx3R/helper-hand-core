from domain.dto.input import ContractorInputDTO
from domain.dto.user.request.user_registration_dto import (
    TelegramUserRegistrationDTO,
    UserRegistrationDTO,
    UserResetDTO,
    WebUserRegistrationDTO,
)


class ContractorRegistrationDTO(ContractorInputDTO, UserRegistrationDTO):
    pass


class ContractorResetDTO(ContractorInputDTO, UserResetDTO):
    pass


class WebContractorRegistrationDTO(
    WebUserRegistrationDTO, ContractorRegistrationDTO
):
    pass


class TelegramContractorRegistrationDTO(
    TelegramUserRegistrationDTO, ContractorRegistrationDTO
):
    pass

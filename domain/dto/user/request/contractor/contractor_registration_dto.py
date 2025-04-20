from domain.dto.user.request.user_input_dto import UserInputDTO
from domain.dto.user.request.user_registration_dto import (
    TelegramUserRegistrationDTO,
    UserRegistrationDTO,
    UserResetDTO,
    WebUserRegistrationDTO,
)


class ContractorInputDTO(UserInputDTO):
    about: str


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

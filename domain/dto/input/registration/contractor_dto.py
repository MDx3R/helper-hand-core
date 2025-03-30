from domain.dto.input import ContractorInputDTO
from .user_dto import UserRegistrationDTO, UserResetDTO, WebUserRegistrationDTO, TelegramUserRegistrationDTO

class ContractorRegistrationDTO(ContractorInputDTO, UserRegistrationDTO):
    pass

class ContractorResetDTO(ContractorInputDTO, UserResetDTO):
    pass

class WebContractorRegistrationDTO(WebUserRegistrationDTO, ContractorRegistrationDTO):
    pass

class TelegramContractorRegistrationDTO(TelegramUserRegistrationDTO, ContractorRegistrationDTO):
    pass
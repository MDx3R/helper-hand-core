from domain.dto.input import ContracteeInputDTO
from .user_dto import UserRegistrationDTO, UserResetDTO, WebUserRegistrationDTO, TelegramUserRegistrationDTO

class ContracteeRegistrationDTO(ContracteeInputDTO, UserRegistrationDTO):
    pass
    
class ContracteeResetDTO(ContracteeRegistrationDTO, UserResetDTO):
    pass

class WebContracteeRegistrationDTO(WebUserRegistrationDTO, ContracteeRegistrationDTO):
    pass

class TelegramContracteeRegistrationDTO(TelegramUserRegistrationDTO, ContracteeRegistrationDTO):
    pass
from pydantic import Field

from domain.entities import Contractor 
from domain.entities.enums import RoleEnum

from .user_dto import UserRegistrationDTO, UserResetDTO, WebUserRegistrationDTO, TelegramUserRegistrationDTO

class ContractorRegistrationDTO(UserRegistrationDTO):
    about: str
    role: RoleEnum = Field(default=RoleEnum.contractor, frozen=True)

    def to_contractor(self) -> Contractor:
        """
        Поле `status` устанавливается значением по умолчанию.
        """
        return Contractor.model_validate(self.model_dump())

class ContractorResetDTO(UserResetDTO, ContractorRegistrationDTO):
    user_id: int = Field(alias="contractor_id")

    def to_contractor(self) -> Contractor:
        """
        Поле `status` устанавливается значением по умолчанию.
        """
        return Contractor.model_validate(self.model_dump(by_alias=True) | {"user_id": self.user_id})

class WebContractorRegistrationDTO(WebUserRegistrationDTO, ContractorRegistrationDTO):
    pass

class TelegramContractorRegistrationDTO(TelegramUserRegistrationDTO, ContractorRegistrationDTO):
    pass

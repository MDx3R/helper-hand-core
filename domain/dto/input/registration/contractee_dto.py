from pydantic import Field

from typing import List
from datetime import date

from domain.entities import Contractee 
from domain.entities.enums import RoleEnum, GenderEnum, CitizenshipEnum, PositionEnum

from .user_dto import UserRegistrationDTO, UserResetDTO, WebUserRegistrationDTO, TelegramUserRegistrationDTO

class ContracteeRegistrationDTO(UserRegistrationDTO):
    birthday: date
    height: int
    gender: GenderEnum
    citizenship: CitizenshipEnum
    positions: List[PositionEnum]
    role: RoleEnum = Field(default=RoleEnum.contractee, frozen=True)

    def to_contractee(self) -> Contractee:
        """
        Поле `status` устанавливается значением по умолчанию.
        """
        return Contractee.model_validate(self.model_dump())
    
class ContracteeResetDTO(UserResetDTO, ContracteeRegistrationDTO):
    user_id: int = Field(alias="contractee_id")

    def to_contractee(self) -> Contractee:
        """
        Поле `status` устанавливается значением по умолчанию.
        """
        return Contractee.model_validate(self.model_dump(by_alias=True) | {"user_id": self.user_id})

class WebContracteeRegistrationDTO(WebUserRegistrationDTO, ContracteeRegistrationDTO):
    pass

class TelegramContracteeRegistrationDTO(TelegramUserRegistrationDTO, ContracteeRegistrationDTO):
    pass
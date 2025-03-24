from typing import List
from datetime import date

from domain.entities import Contractee 
from domain.entities.enums import RoleEnum, GenderEnum, CitizenshipEnum, PositionEnum

from .user_dto import UserInputDTO

class ContracteeInputDTO(UserInputDTO):
    birthday: date
    height: int
    gender: GenderEnum
    citizenship: CitizenshipEnum
    positions: List[PositionEnum]
    role: RoleEnum = RoleEnum.contractee

    def to_contractee(self) -> Contractee:
        """
        Поле `status` устанавливается значением по умолчанию.
        """
        return Contractee.model_validate(self.model_dump())
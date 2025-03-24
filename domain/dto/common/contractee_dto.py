from typing import List
from datetime import date

from .user_dto import UserDTO

from domain.entities import Contractee
from domain.entities.enums import RoleEnum, GenderEnum, CitizenshipEnum, PositionEnum

class ContracteeDTO(UserDTO):
    birthday: date
    height: int
    gender: GenderEnum
    citizenship: CitizenshipEnum
    positions: List[PositionEnum]
    role: RoleEnum

    @property
    def contractee_id(self) -> int:
        return self.user_id
    
    @classmethod
    def from_contractee(cls, contractee: Contractee) -> 'ContracteeDTO':
        return cls.from_model(contractee)
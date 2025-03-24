from .user_dto import UserDTO

from domain.entities import Contractor
from domain.entities.enums import RoleEnum

class ContractorDTO(UserDTO):
    about: str
    role: RoleEnum
    
    @property
    def contractor_id(self) -> int:
        return self.user_id
    
    @classmethod
    def from_contractor(cls, contractor: Contractor) -> 'ContractorDTO':
        return cls.from_model(contractor)
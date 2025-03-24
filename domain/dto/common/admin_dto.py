from typing import Optional
from .user_dto import UserDTO

from domain.entities import Admin
from domain.entities.enums import RoleEnum

class AdminDTO(UserDTO):
    about: str
    role: RoleEnum
    contractor_id: Optional[int] = None
    
    @property
    def contractor_id(self) -> int:
        return self.user_id
    
    @classmethod
    def from_admin(cls, admin: Admin) -> 'AdminDTO':
        return cls.from_model(admin)
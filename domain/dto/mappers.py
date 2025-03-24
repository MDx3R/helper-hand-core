from domain.entities import User
from domain.entities.enums import RoleEnum

from domain.dto.common import UserDTO, ContracteeDTO, ContractorDTO, AdminDTO

def map_user_to_dto(user: User) -> UserDTO | None:
    mapping = {
        RoleEnum.contractee: ContracteeDTO.from_contractee,
        RoleEnum.contractor: ContractorDTO.from_contractor,
        RoleEnum.admin: AdminDTO.from_admin,
    }
    return mapping.get(user.role, lambda x: None)(user)
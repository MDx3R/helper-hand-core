from domain.entities import User
from domain.entities.enums import RoleEnum

from application.dtos.output import UserOutputDTO, ContracteeOutputDTO, ContractorOutputDTO, AdminOutputDTO

def map_user_to_dto(user: User) -> UserOutputDTO | None:
    mapping = {
        RoleEnum.contractee: ContracteeOutputDTO.from_contractee,
        RoleEnum.contractor: ContractorOutputDTO.from_contractor,
        RoleEnum.admin: AdminOutputDTO.from_admin,
    }
    return mapping.get(user.role, lambda x: None)(user)
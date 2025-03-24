from domain.entities import Contractor 
from domain.entities.enums import RoleEnum

from .user_dto import UserInputDTO

class ContractorInputDTO(UserInputDTO):
    about: str
    role: RoleEnum = RoleEnum.contractor

    def to_contractor(self) -> Contractor:
        """
        Поле `status` устанавливается значением по умолчанию.
        """
        return Contractor.model_validate(self.model_dump())
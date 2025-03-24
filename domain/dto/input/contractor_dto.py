from pydantic import Field

from domain.entities import Contractor 
from domain.entities.enums import RoleEnum

from .user_dto import UserInputDTO

class ContractorInputDTO(UserInputDTO):
    about: str
    role: RoleEnum = Field(default=RoleEnum.contractor, frozen=True)

    def to_contractor(self, contractor_id: int | None = None) -> Contractor:
        """
        Поле `status` устанавливается значением по умолчанию.
        """
        return Contractor.model_validate(self.model_dump() | {"contractor_id": contractor_id})
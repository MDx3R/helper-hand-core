from domain.entities import Contractee
from domain.services.user import ContracteeUserService

from domain.dto.common import ContracteeDTO

class ContracteeUserServiceImpl(ContracteeUserService):
    async def get_profile(self, contractee: Contractee) -> Contractee:
        return ContracteeDTO.from_contractee(contractee)
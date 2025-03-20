from domain.entities import Contractee
from domain.services.user import ContracteeUserService

from application.dtos.output import ContracteeOutputDTO

class ContracteeUserServiceImpl(ContracteeUserService):
    async def get_profile(self, contractee: Contractee) -> Contractee:
        return ContracteeOutputDTO.from_contractee(contractee)
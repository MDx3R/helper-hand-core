from domain.services.user import ContracteeUserQueryService
from domain.dto.common import ContracteeDTO
from domain.dto.context import UserContextDTO

from application.usecases.user import GetContracteeUseCase

class ContracteeUserQueryServiceImpl(ContracteeUserQueryService):
    def __init__(
        self, 
        get_contractee_use_case: GetContracteeUseCase,
    ):
        self.get_contractee_use_case = get_contractee_use_case

    async def get_profile(self, context: UserContextDTO) -> ContracteeDTO:
        return self.get_contractee_use_case.get_contractee(context.user_id)
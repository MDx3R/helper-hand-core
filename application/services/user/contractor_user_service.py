from domain.services.user import ContractorUserQueryService
from domain.dto.common import ContractorDTO, ContracteeDTO
from domain.dto.context import UserContextDTO

from application.usecases.user import GetContracteeUseCase, GetContractorUseCase

class ContractorUserQueryServiceImpl(ContractorUserQueryService):
    def __init__(
        self, 
        get_contractee_use_case: GetContracteeUseCase,
        get_contractor_use_case: GetContractorUseCase
    ):
        self.get_contractor_use_case = get_contractor_use_case
        self.get_contractee_use_case = get_contractee_use_case

    async def get_user(self, user_id: int, context: UserContextDTO) -> ContractorDTO | ContracteeDTO | None:
        if user_id == context.user_id:
            return await self.get_profile(context)
        
        return await self.get_contractee_use_case.get_contractee(user_id)

    async def get_profile(self, context: UserContextDTO) -> ContractorDTO:
        return await self.get_contractor_use_case.get_contractor(context.user_id)
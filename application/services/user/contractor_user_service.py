from application.services.user.user_query_service import BaseUserQueryService
from application.usecases.user.contractor.get_user_use_case import (
    GetProfileForContractorUseCase,
    GetUserForContractorUseCase,
)
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.response.contractor.contractor_output_dto import (
    CompleteContractorOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    CompleteContractorOutputDTO,
)
from domain.services.user.contractor_user_service import (
    ContractorUserQueryService,
)


class ContractorUserQueryServiceImpl(
    BaseUserQueryService, ContractorUserQueryService
):
    def __init__(
        self,
        get_user_use_case: GetUserForContractorUseCase,
        get_profile_use_case: GetProfileForContractorUseCase,
    ):
        super().__init__(get_user_use_case)
        self.get_profile_use_case = get_profile_use_case

    async def get_profile(
        self, context: UserContextDTO
    ) -> CompleteContractorOutputDTO:
        return await self.get_profile_use_case.execute(context)

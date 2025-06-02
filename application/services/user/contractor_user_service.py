from application.services.user.user_query_service import BaseUserQueryService
from application.usecases.user.contractor.get_user_use_case import (
    GetProfileForContractorUseCase,
    GetUserForContractorUseCase,
)
from application.usecases.user.update_user_use_case import (
    UpdateContractorUseCase,
)
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.request.contractor.contractor_registration_dto import (
    UpdateContractorDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    CompleteContractorOutputDTO,
    ContractorOutputDTO,
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
        update_contractor_use_case: UpdateContractorUseCase,
    ):
        super().__init__(get_user_use_case)
        self.get_profile_use_case = get_profile_use_case
        self.update_contractor_use_case = update_contractor_use_case

    async def get_profile(
        self, context: UserContextDTO
    ) -> CompleteContractorOutputDTO:
        return await self.get_profile_use_case.execute(context)

    async def update_profile(
        self, query: UpdateContractorDTO
    ) -> ContractorOutputDTO:
        return await self.update_contractor_use_case.execute(query)

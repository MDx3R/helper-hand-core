from application.services.user.user_query_service import BaseUserQueryService
from application.usecases.user.contractee.get_user_use_case import (
    GetProfileForContracteeUseCase,
    GetUserForContracteeUseCase,
)
from application.usecases.user.update_user_use_case import (
    UpdateContracteeUseCase,
)
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.request.contractee.contractee_registration_dto import (
    UpdateContracteeDTO,
)
from domain.dto.user.response.contractee.contractee_output_dto import (
    CompleteContracteeOutputDTO,
    ContracteeOutputDTO,
)
from domain.services.user.contractee_user_service import (
    ContracteeUserQueryService,
)


class ContracteeUserQueryServiceImpl(
    BaseUserQueryService, ContracteeUserQueryService
):
    def __init__(
        self,
        get_user_use_case: GetUserForContracteeUseCase,
        get_profile_use_case: GetProfileForContracteeUseCase,
        update_contractee_use_case: UpdateContracteeUseCase,
    ):
        super().__init__(get_user_use_case)
        self.get_profile_use_case = get_profile_use_case
        self.update_contractee_use_case = update_contractee_use_case

    async def get_profile(
        self, context: UserContextDTO
    ) -> CompleteContracteeOutputDTO:
        return await self.get_profile_use_case.execute(context)

    async def update_profile(
        self, query: UpdateContracteeDTO
    ) -> ContracteeOutputDTO:
        return await self.update_contractee_use_case.execute(query)

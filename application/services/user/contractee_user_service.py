from application.services.user.user_query_service import BaseUserQueryService
from application.usecases.user.contractee.get_user_use_case import (
    GetProfileForContracteeUseCase,
    GetUserForContracteeUseCase,
)
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.response.contractee.contractee_output_dto import (
    CompleteContracteeOutputDTO,
)
from domain.services.user.contractee_user_service import (
    ContracteeUserQueryService,
)


class ContracteeUserQueryServiceImpl(
    ContracteeUserQueryService, BaseUserQueryService
):
    def __init__(
        self,
        get_user_use_case: GetUserForContracteeUseCase,
        get_profile_use_case: GetProfileForContracteeUseCase,
    ):
        super().__init__(get_user_use_case)
        self.get_profile_use_case = get_profile_use_case

    async def get_profile(
        self, context: UserContextDTO
    ) -> CompleteContracteeOutputDTO:
        return await self.get_profile_use_case.execute(context)

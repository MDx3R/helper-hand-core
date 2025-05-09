from application.usecases.user.user_query_use_case import GetUserUseCase
from domain.dto.user.internal.user_query_dto import GetUserDTO
from domain.dto.user.response.admin.admin_output_dto import (
    CompleteAdminOutputDTO,
)
from domain.dto.user.response.contractee.contractee_output_dto import (
    CompleteContracteeOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    CompleteContractorOutputDTO,
)


class BaseUserQueryService:
    def __init__(
        self,
        get_user_use_case: GetUserUseCase,
    ):
        self.get_user_use_case = get_user_use_case

    async def get_user(
        self, query: GetUserDTO
    ) -> (
        CompleteAdminOutputDTO
        | CompleteContracteeOutputDTO
        | CompleteContractorOutputDTO
        | None
    ):
        return await self.get_user_use_case.execute(query)

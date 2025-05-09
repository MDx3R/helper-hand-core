from application.usecases.user.user_query_use_case import GetUserUseCase
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.response.contractor.contractor_output_dto import (
    CompleteContractorOutputDTO,
)


class GetUserForContractorUseCase(GetUserUseCase):
    pass


class GetProfileForContractorUseCase:
    async def execute(
        self, context: UserContextDTO
    ) -> CompleteContractorOutputDTO:
        pass

from application.usecases.user.user_query_use_case import GetUserUseCase
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.response.contractee.contractee_output_dto import (
    CompleteContracteeOutputDTO,
)


class GetUserForContracteeUseCase(GetUserUseCase):
    pass


class GetProfileForContracteeUseCase:
    async def execute(
        self, context: UserContextDTO
    ) -> CompleteContracteeOutputDTO:
        pass

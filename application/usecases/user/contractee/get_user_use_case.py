from application.usecases.user.user_query_use_case import (
    GetCompleteUserUseCase,
)
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.response.contractee.contractee_output_dto import (
    CompleteContracteeOutputDTO,
)
from domain.mappers.user_mappers import ContracteeMapper
from domain.repositories.user.contractee.contractee_query_repository import (
    ContracteeQueryRepository,
)


class GetUserForContracteeUseCase(GetCompleteUserUseCase):
    pass


class GetProfileForContracteeUseCase:
    def __init__(self, repository: ContracteeQueryRepository):
        self.repository = repository

    async def execute(
        self, context: UserContextDTO
    ) -> CompleteContracteeOutputDTO:
        contractee = await self.repository.get_complete_contractee(
            context.user_id
        )
        return ContracteeMapper.to_complete(contractee)

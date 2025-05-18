from application.usecases.user.user_query_use_case import (
    GetCompleteUserUseCase,
)
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.response.contractor.contractor_output_dto import (
    CompleteContractorOutputDTO,
)
from domain.mappers.user_mappers import ContractorMapper
from domain.repositories.user.contractor.contractor_query_repository import (
    ContractorQueryRepository,
)


class GetUserForContractorUseCase(GetCompleteUserUseCase):
    pass


class GetProfileForContractorUseCase:
    def __init__(self, repository: ContractorQueryRepository):
        self.repository = repository

    async def execute(
        self, context: UserContextDTO
    ) -> CompleteContractorOutputDTO:
        contractor = await self.repository.get_complete_contractor(
            context.user_id
        )
        return ContractorMapper.to_complete(contractor)

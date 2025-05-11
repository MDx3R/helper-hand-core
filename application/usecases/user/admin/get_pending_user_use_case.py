from domain.dto.user.response.contractee.contractee_output_dto import (
    CompleteContracteeOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    CompleteContractorOutputDTO,
)
from domain.mappers.user_mappers import UserRoleMapper
from domain.repositories.user.user_role_query_repository import (
    UserRoleQueryRepository,
)


class GetPendingUserUseCase:
    def __init__(self, repository: UserRoleQueryRepository):
        self.repository = repository

    async def execute(
        self,
    ) -> CompleteContracteeOutputDTO | CompleteContractorOutputDTO:
        user = await self.repository.get_first_pending_user()
        return UserRoleMapper.to_complete(user)

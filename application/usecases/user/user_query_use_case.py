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
from domain.mappers.user_mappers import UserRoleMapper
from domain.repositories.user.user_role_query_repository import (
    UserRoleQueryRepository,
)


class GetUserUseCase:
    def __init__(self, repository: UserRoleQueryRepository):
        self.repository = repository

    async def execute(
        self, query: GetUserDTO
    ) -> (
        CompleteContracteeOutputDTO
        | CompleteContractorOutputDTO
        | CompleteAdminOutputDTO
        | None
    ):
        user = await self.repository.get_complete_user(query.user_id)
        if not user:
            return None

        return UserRoleMapper.to_complete(user)

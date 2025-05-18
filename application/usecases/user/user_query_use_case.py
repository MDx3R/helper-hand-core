from domain.dto.user.internal.user_context_dto import UserContextDTO
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
from domain.dto.user.response.user_output_dto import UserOutputDTO
from domain.exceptions.base import ServiceException
from domain.mappers.user_mappers import UserMapper, UserRoleMapper
from domain.repositories.user.user_query_repository import UserQueryRepository
from domain.repositories.user.user_role_query_repository import (
    UserRoleQueryRepository,
)


class GetProfileForUserUseCase:
    def __init__(self, repository: UserQueryRepository):
        self.repository = repository

    async def execute(self, context: UserContextDTO) -> UserOutputDTO | None:
        user = await self.repository.get_user(context.user_id)
        if not user:
            raise ServiceException

        return UserMapper.to_output(user)


class GetCompleteUserUseCase:
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

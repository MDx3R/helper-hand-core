from typing import List
from domain.dto.user.internal.user_context_dto import PaginatedDTO
from domain.dto.user.internal.user_filter_dto import UserFilterDTO
from domain.dto.user.response.contractee.contractee_output_dto import (
    CompleteContracteeOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    CompleteContractorOutputDTO,
)
from domain.dto.user.response.user_output_dto import UserOutputDTO
from domain.entities.user.enums import UserStatusEnum
from domain.mappers.user_mappers import UserMapper, UserRoleMapper
from domain.repositories.user.user_query_repository import UserQueryRepository
from domain.repositories.user.user_role_query_repository import (
    UserRoleQueryRepository,
)


class GetPendingUserUseCase:
    def __init__(self, repository: UserRoleQueryRepository):
        self.repository = repository

    async def execute(
        self,
    ) -> CompleteContracteeOutputDTO | CompleteContractorOutputDTO | None:
        users = await self.repository.filter_users(
            UserFilterDTO(size=1, status=UserStatusEnum.pending)
        )
        if not users:
            return None
        return UserRoleMapper.to_complete(users[-1])


class ListPendingUsersUseCase:
    def __init__(self, repository: UserQueryRepository):
        self.repository = repository

    async def execute(self, query: PaginatedDTO) -> List[UserOutputDTO]:
        users = await self.repository.filter_users(
            UserFilterDTO(
                last_id=query.last_id,
                size=query.size,
                status=UserStatusEnum.pending,
            )
        )
        return [UserMapper.to_output(i) for i in users]

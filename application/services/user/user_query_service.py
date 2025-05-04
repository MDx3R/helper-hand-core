from typing import List
from application.usecases.user.user_query_use_case import (
    GetCompleteUserWithRoleUseCase,
)
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.internal.user_filter_dto import UserFilterDTO
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
from domain.services.user.user_query_service import UserQueryService


class UserQueryServiceImpl(UserQueryService):
    def __init__(self, get_user_use_case: GetCompleteUserWithRoleUseCase):
        self.get_user_use_case = get_user_use_case
        # TODO: UseCase (filter_users)

    async def get_user(
        self, query: GetUserDTO
    ) -> (
        CompleteAdminOutputDTO
        | CompleteContracteeOutputDTO
        | CompleteContractorOutputDTO
        | None
    ):
        return await self.get_user_use_case.execute(query)

    async def filter_users(self, query: UserFilterDTO) -> List[UserOutputDTO]:
        pass

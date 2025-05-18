from application.usecases.user.user_query_use_case import (
    GetCompleteUserUseCase,
)
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
from domain.mappers.user_mappers import AdminMapper
from domain.repositories.user.admin.admin_query_repository import (
    AdminQueryRepository,
)


class GetUserForAdminUseCase(GetCompleteUserUseCase):
    pass


class GetProfileForAdminUseCase:
    def __init__(self, repository: AdminQueryRepository):
        self.repository = repository

    async def execute(self, context: UserContextDTO) -> CompleteAdminOutputDTO:
        admin = await self.repository.get_complete_admin(context.user_id)
        return AdminMapper.to_complete(admin)

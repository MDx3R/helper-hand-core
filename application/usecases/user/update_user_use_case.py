from application.transactions import transactional
from domain.dto.user.request.admin.create_admin_dto import UpdateAdminDTO
from domain.dto.user.request.contractee.contractee_registration_dto import (
    UpdateContracteeDTO,
)
from domain.dto.user.request.contractor.contractor_registration_dto import (
    UpdateContractorDTO,
)
from domain.dto.user.response.admin.admin_output_dto import AdminOutputDTO
from domain.dto.user.response.contractee.contractee_output_dto import (
    ContracteeOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    ContractorOutputDTO,
)
from domain.exceptions.base import ServiceException
from domain.mappers.user_mappers import (
    AdminMapper,
    ContracteeMapper,
    ContractorMapper,
)
from domain.repositories.user.admin.admin_command_repository import (
    AdminCommandRepository,
)
from domain.repositories.user.admin.admin_query_repository import (
    AdminQueryRepository,
)
from domain.repositories.user.contractee.contractee_command_repository import (
    ContracteeCommandRepository,
)
from domain.repositories.user.contractee.contractee_query_repository import (
    ContracteeQueryRepository,
)
from domain.repositories.user.contractor.contractor_command_repository import (
    ContractorCommandRepository,
)
from domain.repositories.user.contractor.contractor_query_repository import (
    ContractorQueryRepository,
)


class UpdateAdminUseCase:
    def __init__(
        self,
        admin_query_repository: AdminQueryRepository,
        admin_command_repository: AdminCommandRepository,
    ) -> None:
        self.admin_query_repository = admin_query_repository
        self.admin_command_repository = admin_command_repository

    @transactional
    async def execute(self, request: UpdateAdminDTO) -> AdminOutputDTO:
        user = await self.admin_query_repository.get_admin(
            request.context.user_id
        )
        if not user:
            raise ServiceException("Непредвиденная ошибка")

        user = user.model_copy(update=request.user.model_dump())
        user = await self.admin_command_repository.update_admin(user)
        return AdminMapper.to_output(user)


class UpdateContracteeUseCase:
    def __init__(
        self,
        contractee_query_repository: ContracteeQueryRepository,
        contractee_command_repository: ContracteeCommandRepository,
    ) -> None:
        self.contractee_query_repository = contractee_query_repository
        self.contractee_command_repository = contractee_command_repository

    @transactional
    async def execute(
        self, request: UpdateContracteeDTO
    ) -> ContracteeOutputDTO:
        user = await self.contractee_query_repository.get_contractee(
            request.context.user_id
        )
        if not user:
            raise ServiceException("Непредвиденная ошибка")

        user = user.model_copy(update=request.user.model_dump())
        user = await self.contractee_command_repository.update_contractee(user)
        return ContracteeMapper.to_output(user)


class UpdateContractorUseCase:
    def __init__(
        self,
        contractor_query_repository: ContractorQueryRepository,
        contractor_command_repository: ContractorCommandRepository,
    ) -> None:
        self.contractor_query_repository = contractor_query_repository
        self.contractor_command_repository = contractor_command_repository

    @transactional
    async def execute(
        self, request: UpdateContractorDTO
    ) -> ContractorOutputDTO:
        user = await self.contractor_query_repository.get_contractor(
            request.context.user_id
        )
        if not user:
            raise ServiceException("Непредвиденная ошибка")

        user = user.model_copy(update=request.user.model_dump())
        user = await self.contractor_command_repository.update_contractor(user)
        return ContractorMapper.to_output(user)

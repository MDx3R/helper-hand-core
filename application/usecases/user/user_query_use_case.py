from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from domain.dto.user.internal.user_query_dto import GetUserDTO
from domain.dto.user.response.admin.admin_output_dto import (
    AdminOutputDTO,
    AdminProfileOutputDTO,
    CompleteAdminOutputDTO,
)
from domain.dto.user.response.contractee.contractee_output_dto import (
    CompleteContracteeOutputDTO,
    ContracteeOutputDTO,
    ContracteeProfileOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    CompleteContractorOutputDTO,
    ContractorOutputDTO,
    ContractorProfileOutputDTO,
)
from domain.dto.user.response.user_output_dto import (
    UserOutputDTO,
    UserProfileOutputDTO,
)

from domain.mappers.user_mappers import AdminMapper, UserMapper, UserRoleMapper
from domain.repositories.user.admin.admin_query_repository import (
    AdminQueryRepository,
)
from domain.repositories.user.contractee.contractee_query_repository import (
    ContracteeQueryRepository,
)
from domain.repositories.user.contractor.contractor_query_repository import (
    ContractorQueryRepository,
)
from domain.repositories.user.user_query_repository import UserQueryRepository
from domain.repositories.user.user_role_query_repository import (
    UserRoleQueryRepository,
)

T = TypeVar("T")
R = TypeVar("R")


class BaseGetUserUseCase(ABC, Generic[T, R]):
    def __init__(self, repository: R):
        self.repository = repository

    async def execute(self, query: GetUserDTO) -> T | None:
        user = await self._get_user(query)
        if not user:
            return None
        return self._map_user(user)

    @abstractmethod
    async def _get_user(self, query: GetUserDTO):
        pass

    @abstractmethod
    def _map_user(self, user) -> T:
        pass


class GetUserProfileUseCase(
    BaseGetUserUseCase[UserProfileOutputDTO, UserQueryRepository]
):
    async def _get_user(self, query: GetUserDTO):
        return await self.repository.get_user(query.user_id)

    def _map_user(self, user) -> UserProfileOutputDTO:
        return UserMapper.to_profile(user)


class GetUserUseCase(BaseGetUserUseCase[UserOutputDTO, UserQueryRepository]):
    async def _get_user(self, query: GetUserDTO):
        return await self.repository.get_user(query.user_id)

    def _map_user(self, user) -> UserOutputDTO:
        return UserMapper.to_output(user)


class GetUserWithRoleProfileUseCase(
    BaseGetUserUseCase[
        ContracteeProfileOutputDTO
        | ContractorProfileOutputDTO
        | AdminProfileOutputDTO,
        UserRoleQueryRepository,
    ]
):
    async def _get_user(self, query: GetUserDTO):
        return await self.repository.get_user(query.user_id)

    def _map_user(
        self, user
    ) -> (
        ContracteeProfileOutputDTO
        | ContractorProfileOutputDTO
        | AdminProfileOutputDTO
    ):
        return UserRoleMapper.to_profile(user)


class GetUserWithRoleUseCase(
    BaseGetUserUseCase[
        ContracteeOutputDTO | ContractorOutputDTO | AdminOutputDTO,
        UserRoleQueryRepository,
    ]
):
    async def _get_user(self, query: GetUserDTO):
        return await self.repository.get_user(query.user_id)

    def _map_user(
        self, user
    ) -> ContracteeOutputDTO | ContractorOutputDTO | AdminOutputDTO:
        return UserRoleMapper.to_output(user)


class GetCompleteUserWithRoleUseCase(
    BaseGetUserUseCase[
        CompleteContracteeOutputDTO
        | CompleteContractorOutputDTO
        | CompleteAdminOutputDTO,
        UserRoleQueryRepository,
    ]
):
    async def _get_user(self, query: GetUserDTO):
        return await self.repository.get_complete_user(query.user_id)

    def _map_user(
        self, user
    ) -> (
        CompleteContracteeOutputDTO
        | CompleteContractorOutputDTO
        | CompleteAdminOutputDTO
    ):
        return UserRoleMapper.to_complete(user)


class GetAdminProfileUseCase(
    BaseGetUserUseCase[AdminProfileOutputDTO, AdminQueryRepository]
):
    async def _get_user(self, query: GetUserDTO):
        return await self.repository.get_admin(query.user_id)

    def _map_user(self, user) -> AdminProfileOutputDTO:
        return AdminMapper.to_profile(user)


class GetAdminUseCase(
    BaseGetUserUseCase[AdminOutputDTO, AdminQueryRepository]
):
    async def _get_user(self, query: GetUserDTO):
        return await self.repository.get_admin(query.user_id)

    def _map_user(self, user) -> AdminOutputDTO:
        return AdminMapper.to_output(user)


class GetCompleteAdminUseCase(
    BaseGetUserUseCase[CompleteAdminOutputDTO, AdminQueryRepository]
):
    async def _get_user(self, query: GetUserDTO):
        return await self.repository.get_complete_admin(query.user_id)

    def _map_user(self, user) -> CompleteAdminOutputDTO:
        return AdminMapper.to_complete(user)


class GetContracteeProfileUseCase(
    BaseGetUserUseCase[ContracteeProfileOutputDTO, ContracteeQueryRepository]
):
    async def _get_user(self, query: GetUserDTO):
        return await self.repository.get_contractee(query.user_id)

    def _map_user(self, user) -> ContracteeProfileOutputDTO:
        return UserRoleMapper.to_profile(user)


class GetContracteeUseCase(
    BaseGetUserUseCase[ContracteeOutputDTO, ContracteeQueryRepository]
):
    async def _get_user(self, query: GetUserDTO):
        return await self.repository.get_contractee(query.user_id)

    def _map_user(self, user) -> ContracteeOutputDTO:
        return UserRoleMapper.to_output(user)


class GetCompleteContracteeUseCase(
    BaseGetUserUseCase[CompleteContracteeOutputDTO, ContracteeQueryRepository]
):
    async def _get_user(self, query: GetUserDTO):
        return await self.repository.get_complete_contractee(query.user_id)

    def _map_user(self, user) -> CompleteContracteeOutputDTO:
        return UserRoleMapper.to_complete(user)


class GetContractorProfileUseCase(
    BaseGetUserUseCase[ContractorProfileOutputDTO, ContractorQueryRepository]
):
    async def _get_user(self, query: GetUserDTO):
        return await self.repository.get_contractor(query.user_id)

    def _map_user(self, user) -> ContractorProfileOutputDTO:
        return UserRoleMapper.to_profile(user)


class GetContractorUseCase(
    BaseGetUserUseCase[ContractorOutputDTO, ContractorQueryRepository]
):
    async def _get_user(self, query: GetUserDTO):
        return await self.repository.get_contractor(query.user_id)

    def _map_user(self, user) -> ContractorOutputDTO:
        return UserRoleMapper.to_output(user)


class GetCompleteContractorUseCase(
    BaseGetUserUseCase[CompleteContractorOutputDTO, ContractorQueryRepository]
):
    async def _get_user(self, query: GetUserDTO):
        return await self.repository.get_complete_contractor(query.user_id)

    def _map_user(self, user) -> CompleteContractorOutputDTO:
        return UserRoleMapper.to_complete(user)


class GetPendingUserUseCase:
    def __init__(self, repository: UserRoleQueryRepository):
        self.repository = repository

    async def execute(
        self,
    ) -> CompleteContracteeOutputDTO | CompleteContractorOutputDTO | None:
        user = await self.repository.get_first_pending_user()
        if not user:
            return None
        return UserRoleMapper.to_complete(user)

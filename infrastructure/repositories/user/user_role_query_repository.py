from typing import Optional
from sqlalchemy import Select
from domain.entities.user.admin.admin import Admin
from domain.entities.user.admin.composite_admin import CompleteAdmin
from domain.entities.user.contractee.composite_contractee import (
    CompleteContractee,
)
from domain.entities.user.contractee.contractee import Contractee
from domain.entities.user.contractor.composite_contractor import (
    CompleteContractor,
)
from domain.entities.user.contractor.contractor import Contractor
from domain.entities.user.enums import RoleEnum, UserStatusEnum
from domain.repositories.user.user_role_query_repository import (
    UserRoleQueryRepository,
)
from infrastructure.database.mappers import (
    AggregatedUserMapper,
    CompleteRoleMapper,
)
from infrastructure.database.models import (
    AdminBase,
    ContracteeBase,
    ContractorBase,
    UserBase,
)
from infrastructure.repositories.base import (
    QueryExecutor,
    frozen,
)
from infrastructure.repositories.user.base import (
    UnmappedUser,
    UserOuterJoinStrategy,
    UserQueryBuilder,
)


@frozen(init=False)
class UnmappedRole(UnmappedUser):
    admin: Optional[AdminBase]
    contractee: Optional[ContracteeBase]
    contractor: Optional[ContractorBase]

    @property
    def role(self):
        match self.user.role:
            case RoleEnum.admin:
                result = self.admin
            case RoleEnum.contractee:
                result = self.contractee
            case RoleEnum.contractor:
                result = self.contractor
            case _:
                result = None

        if not result:
            raise Exception(
                f"Роль пользователя {self.user.user_id} отсутсвует таблице"
            )

        return result


class UserRoleQueryRepositoryImpl(UserRoleQueryRepository):
    def __init__(
        self,
        executor: QueryExecutor,
    ):
        self.executor = executor
        self.strategy = UserOuterJoinStrategy()

    async def get_user(
        self, user_id: int
    ) -> Admin | Contractee | Contractor | None:
        query_builder = self._get_query_buider()
        stmt = (
            query_builder.add_admin()
            .add_contractee()
            .add_contractor()
            .where_user_id(user_id)
            .build()
        )

        unmapped_user = await self._execute_one(stmt)
        if not unmapped_user:
            return None

        return AggregatedUserMapper.to_model(
            unmapped_user.user, unmapped_user.role
        )

    async def get_complete_user(
        self, user_id: int
    ) -> CompleteAdmin | CompleteContractee | CompleteContractor | None:
        query_builder = self._get_query_buider()
        stmt = (
            query_builder.add_admin()
            .add_contractee()
            .add_contractor()
            .add_credentials()
            .where_user_id(user_id)
            .build()
        )

        return await self._execute_one_complete_role(stmt)

    async def get_first_pending_user(
        self,
    ) -> CompleteContractee | CompleteContractor | None:
        query_builder = self._get_query_buider()
        stmt = (
            query_builder.add_contractee()
            .add_contractor()
            .add_credentials()
            .build()
            .where(UserBase.status == UserStatusEnum.pending)
            .limit(1)
        )

        return await self._execute_one_complete_role(stmt)

    def _get_query_buider(self) -> UserQueryBuilder:
        return UserQueryBuilder(self.strategy)

    async def _execute_one_complete_role(self, statement: Select):
        unmapped_user = await self._execute_one(statement)
        if not unmapped_user:
            return None

        return CompleteRoleMapper.to_model(
            unmapped_user.user,
            unmapped_user.admin,
            unmapped_user.contractor,
            unmapped_user.contractee,
            unmapped_user.web,
            unmapped_user.telegram,
        )

    async def _execute_one(self, statement: Select) -> UnmappedRole | None:
        row = (await self.executor.execute(statement)).first()
        if not row:
            return None

        return UnmappedRole(row)

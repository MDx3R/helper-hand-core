from typing import Any, Tuple, List, TypeVar, Type
from sqlalchemy import select, update, exists, and_, Select
from sqlalchemy.engine import Result

from domain.repositories import UserRepository
from domain.models import ApplicationModel, User, Admin, Contractee, Contractor
from domain.models.enums import RoleEnum, UserStatusEnum, GenderEnum
from domain.exceptions import ApplicationException

from application.transactions import TransactionManager

from infrastructure.database.models import (
    Base, 
    UserBase, 
    AdminBase, 
    ContracteeBase,
    ContractorBase
)
from infrastructure.database.mappers import UserMapper, AggregatedUserMapper, AdminMapper, ContracteeMapper, ContractorMapper

from infrastructure.repositories.base import SQLAlchemyRepository

UT = TypeVar("UT", bound=User)

class SQLAlchemyUserRepository(UserRepository, SQLAlchemyRepository):
    async def get_user_by_id(self, user_id: int) -> User | None:
        statement = select(UserBase).where(UserBase.user_id == user_id)
        user = await self._execute_scalar_one(statement)

        return UserMapper.to_model(user)

    async def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        statement = select(UserBase).where(UserBase.telegram_id == telegram_id)
        user = await self._execute_scalar_one(statement)
        return UserMapper.to_model(user)

    async def get_user_with_role(self, user_id: int) -> Contractee | Contractor | Admin | None:
        statement = (
            self._get_user_with_role_statement()
            .where(UserBase.user_id == user_id)
        )

        user, role = await self._execute_user_unmapped_role(statement)
        
        return AggregatedUserMapper.to_model(user, role)

    async def get_first_pending_user_with_role(self) -> Contractee | Contractor | Admin | None:
        statement = (
            self._get_user_with_role_statement()
            .where(UserBase.status == UserStatusEnum.pending).limit(1)
        )
        
        user, role = await self._execute_user_unmapped_role(statement)

        return AggregatedUserMapper.to_model(user, role)

    def _get_user_with_role_statement(self):
        return (
            select(
                UserBase,  
                AdminBase,  
                ContracteeBase,  
                ContractorBase  
            )
            .outerjoin(AdminBase, UserBase.user_id == AdminBase.admin_id)
            .outerjoin(ContracteeBase, UserBase.user_id == ContracteeBase.contractee_id)
            .outerjoin(ContractorBase, UserBase.user_id == ContractorBase.contractor_id)
        )

    async def get_admin_by_id(self, admin_id: int) -> Admin | None:
        statement = select(UserBase, AdminBase).join(
            AdminBase, and_(UserBase.user_id == admin_id, UserBase.user_id == AdminBase.admin_id)
        ).where(UserBase.role == RoleEnum.admin)

        user, admin = await self._execute_user_role(statement)
        return AdminMapper.to_model(user, admin)

    async def get_contractee_by_id(self, contractee_id: int) -> Contractee | None:
        statement = select(UserBase, ContracteeBase).join(
            ContracteeBase, and_(UserBase.user_id == contractee_id, UserBase.user_id == ContracteeBase.contractee_id)
        ).where(UserBase.role == RoleEnum.contractee)

        user, contractee = await self._execute_user_role(statement)
        return ContracteeMapper.to_model(user, contractee)

    async def get_contractor_by_id(self, contractor_id: int) -> Contractor | None:
        statement = select(UserBase, ContractorBase).join(
            ContractorBase, and_(UserBase.user_id == contractor_id, UserBase.user_id == ContractorBase.contractor_id)
        ).where(UserBase.role == RoleEnum.contractor)

        user, contractor = await self._execute_user_role(statement)
        return ContractorMapper.to_model(user, contractor)

    async def _execute_user_role(
        self, 
        statement: Select[Tuple[UserBase, ContracteeBase | ContractorBase | AdminBase]], 
    ) -> Tuple[UserBase, ContracteeBase | ContractorBase | AdminBase] | Tuple[None, None]:
        row = (await self._execute(statement)).first()

        if not row:
            return None, None

        user, related_instance = row
        return user, related_instance
    
    async def _execute_user_unmapped_role(
        self, 
        statement: Select[Tuple[UserBase, AdminBase, ContracteeBase, ContractorBase]], 
    ) -> Tuple[UserBase, ContracteeBase | ContractorBase | AdminBase] | Tuple[None, None]:
        row = (await self._execute(statement)).first()
        if not row:
            return None, None

        user, admin, contractee, contractor = row
        related_instance = {
            RoleEnum.admin: admin,
            RoleEnum.contractee: contractee,
            RoleEnum.contractor: contractor
        }.get(user.role)

        if related_instance is None:
            return None, None
        
        return user, related_instance

    async def get_admins(self) -> List[Admin]:
        statement = select(UserBase, AdminBase).join(AdminBase, UserBase.user_id == AdminBase.admin_id)

        records = await self._execute_many(statement)
        return [AdminMapper.to_model(user, admin) for user, admin in records]

    async def user_exists_by_phone_number(self, phone_number: str) -> bool:
        statement = select(1).where(UserBase.phone_number == phone_number).limit(1)
        result = await self._execute(statement)
        return bool(result.scalar())

    async def save_contractee(self, contractee: Contractee) -> Contractee:
        return await self._save_user(contractee)

    async def save_contractor(self, contractor: Contractor) -> Contractor:
        return await self._save_user(contractor)

    async def _save_user(self, user: UT) -> UT:
        if not user.user_id:
            user_base, role_base = await self._insert_user(user)
        else:
            user_base, role_base = await self._merge_user(user)

        return AggregatedUserMapper.to_model(user_base, role_base)

    async def _insert_user(self, user: Contractee | Contractor | Admin) -> Tuple[UserBase, ContracteeBase | ContractorBase | AdminBase]:
        async with self.transaction_manager.get_session() as session:
            user_base = AggregatedUserMapper.to_user_base(user)
            session.add(user_base)
            await session.flush()
            
            user.user_id = user_base.user_id # явно устанавливаем назначенный id

            role_base = AggregatedUserMapper.to_role_base(user)

            session.add(role_base)
            await session.flush() # вносим изменения без commit

            return user_base, role_base
        
    async def _merge_user(self, user: Contractee | Contractor | Admin) -> Tuple[UserBase, ContracteeBase | ContractorBase | AdminBase]:
        async with self.transaction_manager.get_session() as session:
            merged_user: UserBase = await session.merge(AggregatedUserMapper.to_base(user))
            await session.flush()

            user.user_id = merged_user.user_id # явно устанавливаем назначенный id

            merged_role = await session.merge(AggregatedUserMapper.to_role_base(user))
            await session.flush() # синхронизируем служебные поля

            return merged_user, merged_role
        
    async def change_user_status(self, user_id: int, status: UserStatusEnum) -> User:
        statement = update(UserBase).where(
            UserBase.user_id == user_id
        ).values(status=status).returning(UserBase)
        
        user = (await self._execute(statement)).fetchone()
        return UserMapper.to_model(user)

    async def filter_contractees_by(self, status: UserStatusEnum = None, gender: GenderEnum = None) -> List[Contractee]:
        statement = (
            select(ContracteeBase)
            .join(UserBase, ContracteeBase.contractee_id == UserBase.user_id)
            .where(UserBase.role == RoleEnum.contractee)
        )
        if gender:
            statement = (
                statement
                .where(ContracteeBase.gender == gender)
            )

        users = await self._execute_scalar_many(statement)
        return [UserMapper.to_model(user) for user in users]
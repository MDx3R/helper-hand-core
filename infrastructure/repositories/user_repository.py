from typing import Any, Tuple, List, TypeVar, Type
from sqlalchemy import select, exists, and_, Select
from sqlalchemy.engine import Result

from domain.repositories import UserRepository
from domain.models import ApplicationModel, User, Admin, Contractee, Contractor
from domain.models.enums import RoleEnum
from domain.exceptions import ApplicationException

from application.transactions import TransactionManager

from infrastructure.database.models import (
    Base, 
    UserBase, 
    AdminBase, 
    ContracteeBase,
    ContractorBase
)
from infrastructure.database.mappers import (
    base_to_model, 
    user_base_to_model,
    user_to_base,
    contractee_to_base,
    contractor_to_base,
    admin_to_base
)

from infrastructure.repositories.base import SQLAlchemyRepository

UT = TypeVar("UT", bound=User)

class SQLAlchemyUserRepository(UserRepository, SQLAlchemyRepository):
    async def get_user_by_id(self, user_id: int) -> User | None:
        statement = select(UserBase).where(UserBase.user_id == user_id)
        user = await self._execute_scalar_one(statement)

        return self._map_base_to_user(user)

    async def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        statement = select(UserBase).where(UserBase.telegram_id == telegram_id)
        user = await self._execute_scalar_one(statement)
        return self._map_base_to_user(user)

    async def get_admin_by_id(self, admin_id: int) -> Admin | None:
        statement = select(UserBase, AdminBase).join(
            AdminBase, and_(UserBase.user_id == admin_id, UserBase.user_id == AdminBase.admin_id)
        ).where(UserBase.role == RoleEnum.admin)

        user, admin = await self._execute_user_role(statement)
        return self._map_base_to_admin(user, admin)

    async def get_contractee_by_id(self, contractee_id: int) -> Contractee | None:
        statement = select(UserBase, ContracteeBase).join(
            ContracteeBase, and_(UserBase.user_id == contractee_id, UserBase.user_id == ContracteeBase.contractee_id)
        ).where(UserBase.role == RoleEnum.contractee)

        user, contractee = await self._execute_user_role(statement)
        return self._map_base_to_contractee(user, contractee)

    async def get_contractor_by_id(self, contractor_id: int) -> Contractor | None:
        statement = select(UserBase, ContractorBase).join(
            ContractorBase, and_(UserBase.user_id == contractor_id, UserBase.user_id == ContractorBase.contractor_id)
        ).where(UserBase.role == RoleEnum.contractor)

        user, contractor = await self._execute_user_role(statement)
        return self._map_base_to_contractor(user, contractor)

    async def _execute_user_role(
        self, 
        statement: Select[Tuple[UserBase, ContracteeBase | ContractorBase | AdminBase]], 
    ) -> Tuple[UserBase, ContracteeBase | ContractorBase | AdminBase] | Tuple[None, None]:
        row = (await self._execute(statement)).first()

        if not row:
            return None, None

        user, related_instance = row
        return user, related_instance

    async def get_admins(self) -> List[Admin]:
        statement = select(UserBase, AdminBase).join(AdminBase, UserBase.user_id == AdminBase.admin_id)

        records = await self._execute_many(statement)
        return [self._map_base_to_admin(user, admin) for user, admin in records]

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

        return user_base_to_model(user_base, role_base, type(user))

    async def _insert_user(self, user: Contractee | Contractor | Admin) -> Tuple[UserBase, ContracteeBase | ContractorBase | AdminBase]:
        async with await self.transaction_manager.get_session() as session:
            user_base = self._map_user_to_base(user)
            session.add(user_base)
            await session.flush()
            
            user.user_id = user_base.user_id # явно устанавливаем назначенный id

            role_base = self._map_role_to_base(user)
            session.add(role_base)
            await session.flush() # вносим изменения без commit

            return user_base, role_base
        
    async def _merge_user(self, user: Contractee | Contractor | Admin) -> Tuple[UserBase, ContracteeBase | ContractorBase | AdminBase]:
        async with await self.transaction_manager.get_session() as session:
            merged_user: UserBase = await session.merge(self._map_user_to_base(user))
            await session.flush()

            user.user_id = merged_user.user_id # явно устанавливаем назначенный id

            merged_role = await session.merge(self._map_role_to_base(user))
            await session.flush() # синхронизируем служебные поля

            return merged_user, merged_role
        
    def _map_base_to_user(self, base: UserBase) -> User | None:
        return base_to_model(base, User) if base else None

    def _map_base_to_admin(self, user: UserBase, admin: AdminBase) -> Admin | None:
        return user_base_to_model(user, admin, Admin) if user else None

    def _map_base_to_contractee(self, user: UserBase, contractee: ContracteeBase) -> Contractee | None:
        return user_base_to_model(user, contractee, Contractee) if user else None

    def _map_base_to_contractor(self, user: UserBase, contractor: ContractorBase) -> Contractor | None:
        return user_base_to_model(user, contractor, Contractor) if user else None
    
    def _map_user_to_base(self, user: User) -> UserBase:
        return user_to_base(user)
    
    def _map_contractee_to_base(self, contractee: Contractee) -> ContracteeBase:
        return contractee_to_base(contractee)
    
    def _map_contractor_to_base(self, contractor: Contractor) -> ContractorBase:
        return contractor_to_base(contractor)
    
    def _map_admin_to_base(self, admin: Admin) -> AdminBase:
        return admin_to_base(admin)
    
    def _map_role_to_base(self, user: Contractee | Contractor | Admin) -> ContracteeBase | ContractorBase | AdminBase:
        match user.role:
            case RoleEnum.contractee:
                return self._map_contractee_to_base(user)
            case RoleEnum.contractor:
                return self._map_contractor_to_base(user)
            case RoleEnum.admin:
                return self._map_admin_to_base(user)
            case _:
                raise ApplicationException(f"Неизвестная роль: {user.role}")
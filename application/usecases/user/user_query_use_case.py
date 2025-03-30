from abc import ABC, abstractmethod

from domain.dto.common import UserDTO, AdminDTO, ContracteeDTO, ContractorDTO
from domain.repositories import UserRepository

from application.transactions import transactional

from domain.dto.mappers import map_user_to_dto

class GetUserUseCase(ABC):
    @abstractmethod
    async def get_user(self, user_id: int) -> UserDTO | None:
        pass

class GetUserWithRoleUseCase(ABC):
    @abstractmethod
    async def get_user_with_role(
        self, 
        user_id: int
    ) -> ContracteeDTO | ContractorDTO | AdminDTO | None:
        pass

class GetAdminUseCase(ABC):
    @abstractmethod
    async def get_admin(self, admin_id: int) -> AdminDTO | None:
        pass

class GetContracteeUseCase:
    @abstractmethod
    async def get_contractee(self, contractee_id: int) -> ContracteeDTO | None:
        pass

class GetContractorUseCase:
    @abstractmethod
    async def get_contractor(self, contractor_id: int) -> ContractorDTO | None:
        pass

class GetPendingUserUseCase:
    @abstractmethod
    async def get_pending_user(self) -> ContracteeDTO | ContractorDTO | None:
        pass

class UserQueryUseCaseFacade(
    GetUserUseCase,
    GetAdminUseCase,
    GetContracteeUseCase,
    GetContractorUseCase,
    GetPendingUserUseCase
):
    def __init__(
        self, user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    async def get_user(self, user_id: int) -> UserDTO | None:
        user = await self.user_repository.get_user(user_id)
        if not user:
            return None
        
        return UserDTO.from_user(user)
    
    async def get_user_with_role(
        self, 
        user_id: int
    ) -> ContracteeDTO | ContractorDTO | AdminDTO | None:
        user = await self.user_repository.get_user_with_role(user_id)
        if not user:
            return None
        
        return map_user_to_dto(user)

    async def get_admin(self, admin_id: int) -> AdminDTO | None:
        admin = await self.user_repository.get_admin(admin_id)
        if not admin:
            return None
        
        return AdminDTO.from_admin(admin)
    
    async def get_contractee(self, contractee_id: int) -> ContracteeDTO | None:
        contractee = await self.user_repository.get_contractee(contractee_id)
        if not contractee:
            return None
        
        return ContracteeDTO.from_contractee(contractee)
    
    async def get_contractor(self, contractor_id: int) -> ContractorDTO | None:
        contractor = await self.user_repository.get_contractor(contractor_id)
        if not contractor:
            return None
        
        return ContractorDTO.from_contractor(contractor)
    
    async def get_pending_user(self) -> ContracteeDTO | ContractorDTO | None:
        user = await self.user_repository.get_first_pending_user_with_role()
        if not user:
            return None
        
        return map_user_to_dto(user)
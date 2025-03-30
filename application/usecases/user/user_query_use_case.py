from domain.dto.input.registration import UserRegistrationDTO

from domain.entities import User, Contractee, Contractor, Admin
from domain.entities.enums import UserStatusEnum
from domain.dto.common import UserDTO, AdminDTO, ContracteeDTO, ContractorDTO
from domain.dto.input.registration import (
    UserRegistrationDTO, 
    ContracteeRegistrationDTO, 
    ContractorRegistrationDTO
)
from domain.repositories import UserRepository
from domain.services.domain import UserDomainService
from domain.exceptions.service import (
    UserStatusChangeNotAllowedException, 
    NotFoundException,
    InvalidInputException
)

from application.transactions import transactional

from abc import ABC, abstractmethod

class GetUserUseCase(ABC):
    @abstractmethod
    async def get_user(self, user_id: int) -> UserDTO | None:
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
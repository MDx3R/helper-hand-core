from abc import ABC, abstractmethod

from domain.dto.user.request.contractee.contractee_registration_dto import (
    RegisterContracteeDTO,
)
from domain.dto.user.request.contractor.contractor_registration_dto import (
    RegisterContractorDTO,
)
from domain.dto.user.request.user_auth_dto import LoginUserDTO
from domain.dto.user.response.contractee.contractee_output_dto import (
    ContracteeRegistationOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    ContractorRegistationOutputDTO,
)
from domain.dto.user.response.user_output_dto import AuthOutputDTO


class UserAuthService(ABC):
    @abstractmethod
    async def login(self, request: LoginUserDTO) -> AuthOutputDTO:  # TODO: DTO
        pass

    @abstractmethod
    async def register_contractor(
        self, request: RegisterContractorDTO
    ) -> ContractorRegistationOutputDTO:
        pass

    @abstractmethod
    async def register_contractee(
        self, request: RegisterContracteeDTO
    ) -> ContracteeRegistationOutputDTO:
        pass


class UserVerificationService(ABC):
    @abstractmethod
    async def verify_telegram(self):
        pass

    @abstractmethod
    async def verify_web(self):
        pass

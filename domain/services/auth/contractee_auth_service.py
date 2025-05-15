from abc import ABC, abstractmethod
from application.usecases.user.register_user_use_case import (
    RegisterContracteeUseCase,
)
from application.usecases.user.reset_user_use_case import (
    ResetContracteeUseCase,
)
from domain.dto.user.request.contractee.contractee_registration_dto import (
    RegisterContracteeDTO,
    ResetContracteeDTO,
)
from domain.dto.user.response.contractee.contractee_output_dto import (
    ContracteeOutputDTO,
    ContracteeRegistationOutputDTO,
)


class ContracteeAuthService(ABC):
    @abstractmethod
    async def register_contractee(
        self, request: RegisterContracteeDTO
    ) -> ContracteeRegistationOutputDTO:
        pass

    @abstractmethod
    async def reset_contractee(
        self, request: ResetContracteeDTO
    ) -> ContracteeOutputDTO:
        pass

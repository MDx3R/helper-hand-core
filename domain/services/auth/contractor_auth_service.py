from abc import ABC, abstractmethod
from application.usecases.user.register_user_use_case import (
    RegisterContractorUseCase,
)
from application.usecases.user.reset_user_use_case import (
    ResetContractorUseCase,
)

from domain.dto.user.request.contractor.contractor_registration_dto import (
    RegisterContractorDTO,
    ResetContractorDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    ContractorOutputDTO,
    ContractorRegistationOutputDTO,
)


class ContractorAuthService(ABC):
    @abstractmethod
    async def register_contractor(
        self, request: RegisterContractorDTO
    ) -> ContractorRegistationOutputDTO:
        pass

    @abstractmethod
    async def reset_contractor(
        self, request: ResetContractorDTO
    ) -> ContractorOutputDTO:
        pass

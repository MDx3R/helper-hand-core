from abc import ABC, abstractmethod

from domain.dto.user.request.contractor.contractor_registration_dto import (
    RegisterContractorDTO,
    ResetContractorDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    ContractorOutputDTO,
    ContractorRegistationOutputDTO,
)


class ContractorAuthService(ABC):
    """
    Интерфейс для сервисов аутентификации и авторизации заказчиков.
    """

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

from application.usecases.user.register_user_use_case import (
    RegisterContractorUseCase,
)
from application.usecases.user.reset_user_use_case import (
    ResetContractorUseCase,
)
from domain.services.auth.contractor_auth_service import ContractorAuthService
from domain.dto.user.request.contractor.contractor_registration_dto import (
    RegisterContractorDTO,
    ResetContractorDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    ContractorOutputDTO,
    ContractorRegistationOutputDTO,
)


class ContractorAuthServiceImpl(ContractorAuthService):
    def __init__(
        self,
        register_use_case: RegisterContractorUseCase,
        reset_use_case: ResetContractorUseCase,
    ):
        self.register_use_case = register_use_case
        self.reset_use_case = reset_use_case
        pass

    async def register_contractor(
        self, request: RegisterContractorDTO
    ) -> ContractorRegistationOutputDTO:
        return await self.register_use_case.execute(request)

    async def reset_contractor(
        self, request: ResetContractorDTO
    ) -> ContractorOutputDTO:
        return await self.reset_use_case.execute(request)

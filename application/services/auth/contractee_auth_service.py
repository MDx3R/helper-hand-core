from application.usecases.auth.register_user_use_case import (
    RegisterContracteeUseCase,
)
from application.usecases.auth.reset_user_use_case import (
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
from domain.services.auth.contractee_auth_service import ContracteeAuthService


class ContracteeAuthServiceImpl(ContracteeAuthService):
    def __init__(
        self,
        register_use_case: RegisterContracteeUseCase,
        reset_use_case: ResetContracteeUseCase,
    ):
        self.register_use_case = register_use_case
        self.reset_use_case = reset_use_case
        pass

    async def register_contractee(
        self, request: RegisterContracteeDTO
    ) -> ContracteeRegistationOutputDTO:
        return await self.register_use_case.execute(request)

    async def reset_contractee(
        self, request: ResetContracteeDTO
    ) -> ContracteeOutputDTO:
        return await self.reset_use_case.execute(request)

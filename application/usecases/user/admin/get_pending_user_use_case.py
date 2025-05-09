from domain.dto.user.response.contractee.contractee_output_dto import (
    CompleteContracteeOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    CompleteContractorOutputDTO,
)


class GetPendingUserUseCase:
    async def execute(
        self,
    ) -> CompleteContracteeOutputDTO | CompleteContractorOutputDTO:
        pass

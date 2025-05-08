from typing import Optional
from domain.dto.user.response.contractor.contractor_output_dto import (
    ContractorOutputDTO,
)
from domain.dto.user.response.user_output_dto import (
    UserOutputDTO,
    UserProfileOutputDTO,
    WithCredentialsOutputDTO,
)


class AdminProfileOutputDTO(UserProfileOutputDTO):
    about: str


class AdminOutputDTO(AdminProfileOutputDTO, UserOutputDTO):
    contractor_id: Optional[int] = None


class CompleteAdminOutputDTO(WithCredentialsOutputDTO):
    user: AdminOutputDTO
    contractor: Optional[ContractorOutputDTO] = None

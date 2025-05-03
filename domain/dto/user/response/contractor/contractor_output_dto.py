from domain.dto.base import ApplicationDTO
from domain.dto.user.response.user_output_dto import (
    AuthOutputDTO,
    UserOutputDTO,
    UserProfileOutputDTO,
    WithAuthOutputDTO,
    WithCredentialsOutputDTO,
)


class ContractorProfileOutputDTO(UserProfileOutputDTO):
    about: str


class ContractorOutputDTO(ContractorProfileOutputDTO, UserOutputDTO):
    pass


class CompleteContractorOutputDTO(WithCredentialsOutputDTO):
    contractor: ContractorOutputDTO


class ContractorRegistationOutputDTO(WithAuthOutputDTO):
    contractor: ContractorOutputDTO

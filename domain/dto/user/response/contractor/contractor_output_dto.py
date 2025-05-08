from domain.dto.user.response.user_output_dto import (
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
    user: ContractorOutputDTO


class ContractorRegistationOutputDTO(WithAuthOutputDTO):
    user: ContractorOutputDTO  # TODO: CompleteContractorOutputDTO

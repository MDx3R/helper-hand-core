from domain.dto.user.response.user_output_dto import (
    BaseCompleteUserOutputDTO,
    BaseUserRegistationOutputDTO,
    UserOutputDTO,
    UserProfileOutputDTO,
)


class ContractorProfileOutputDTO(UserProfileOutputDTO):
    about: str


class ContractorOutputDTO(ContractorProfileOutputDTO, UserOutputDTO):
    pass


class CompleteContractorOutputDTO(BaseCompleteUserOutputDTO):
    user: ContractorOutputDTO


class ContractorRegistationOutputDTO(BaseUserRegistationOutputDTO):
    user: CompleteContractorOutputDTO

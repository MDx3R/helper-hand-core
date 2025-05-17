from datetime import date
from typing import List

from domain.dto.user.response.user_output_dto import (
    BaseCompleteUserOutputDTO,
    BaseUserRegistationOutputDTO,
    UserOutputDTO,
    UserProfileOutputDTO,
    WithAuthOutputDTO,
    WithCredentialsOutputDTO,
)
from domain.entities.enums import CitizenshipEnum, GenderEnum, PositionEnum


class ContracteeProfileOutputDTO(UserProfileOutputDTO):
    birthday: date
    height: int
    gender: GenderEnum
    citizenship: CitizenshipEnum
    positions: List[PositionEnum]


class ContracteeOutputDTO(ContracteeProfileOutputDTO, UserOutputDTO):
    pass


class CompleteContracteeOutputDTO(BaseCompleteUserOutputDTO):
    user: ContracteeOutputDTO


class ContracteeRegistationOutputDTO(BaseUserRegistationOutputDTO):
    user: CompleteContracteeOutputDTO

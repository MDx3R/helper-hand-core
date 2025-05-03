from datetime import date
from typing import List

from domain.dto.base import ApplicationDTO
from domain.dto.user.response.user_output_dto import (
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


class CompleteContracteeOutputDTO(WithCredentialsOutputDTO):
    contractee: ContracteeOutputDTO


class ContracteeRegistationOutputDTO(WithAuthOutputDTO):
    contractee: ContracteeOutputDTO

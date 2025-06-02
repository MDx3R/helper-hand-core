from datetime import date
from typing import List
from domain.dto.user.internal.user_context_dto import WithUserContextDTO
from domain.dto.user.request.create_user_dto import BaseCreateUserDTO
from domain.dto.user.request.user_input_dto import (
    BaseRegisterUserDTO,
    UserInputDTO,
)
from domain.entities.enums import CitizenshipEnum, GenderEnum, PositionEnum


class ContracteeInputDTO(UserInputDTO):
    birthday: date
    height: int
    gender: GenderEnum
    citizenship: CitizenshipEnum
    positions: List[PositionEnum]


class RegisterContracteeDTO(BaseRegisterUserDTO):
    user: ContracteeInputDTO


class ResetContracteeDTO(WithUserContextDTO):
    user: ContracteeInputDTO


class CreateContracteeDTO(BaseCreateUserDTO):
    user: ContracteeInputDTO


class UpdateContracteeDTO(WithUserContextDTO):
    user: ContracteeInputDTO

from datetime import date
from typing import List

from pydantic import Field, field_validator
from domain.dto.user.internal.user_context_dto import WithUserContextDTO
from domain.dto.user.request.create_user_dto import BaseCreateUserDTO
from domain.dto.user.request.user_input_dto import (
    BaseRegisterUserDTO,
    UserInputDTO,
)
from domain.entities.enums import CitizenshipEnum, GenderEnum, PositionEnum


class ContracteeInputDTO(UserInputDTO):
    birthday: date
    height: int = Field(..., ge=140, le=230)
    gender: GenderEnum
    citizenship: CitizenshipEnum
    positions: List[PositionEnum]

    @field_validator("birthday")
    @classmethod
    def validate_birthday(cls, v: date) -> date:
        today = date.today()
        if v >= today:
            raise ValueError("Birthday must be in the past")
        return v


class RegisterContracteeDTO(BaseRegisterUserDTO):
    user: ContracteeInputDTO


class ResetContracteeDTO(WithUserContextDTO):
    user: ContracteeInputDTO


class CreateContracteeDTO(BaseCreateUserDTO):
    user: ContracteeInputDTO


class UpdateContracteeDTO(WithUserContextDTO):
    user: ContracteeInputDTO

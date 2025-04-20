from datetime import date
from typing import List
from domain.dto.user.request.user_input_dto import UserInputDTO
from domain.dto.user.request.user_registration_dto import (
    TelegramUserRegistrationDTO,
    UserRegistrationDTO,
    UserResetDTO,
    WebUserRegistrationDTO,
)
from domain.entities.enums import CitizenshipEnum, GenderEnum, PositionEnum


class ContracteeInputDTO(UserInputDTO):
    birthday: date
    height: int
    gender: GenderEnum
    citizenship: CitizenshipEnum
    positions: List[PositionEnum]


class ContracteeRegistrationDTO(ContracteeInputDTO, UserRegistrationDTO):
    pass


class ContracteeResetDTO(ContracteeInputDTO, UserResetDTO):
    pass


class WebContracteeRegistrationDTO(WebUserRegistrationDTO, ContracteeRegistrationDTO):
    pass


class TelegramContracteeRegistrationDTO(
    TelegramUserRegistrationDTO, ContracteeRegistrationDTO
):
    pass

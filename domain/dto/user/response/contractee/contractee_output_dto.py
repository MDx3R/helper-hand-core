from datetime import date
from typing import List

from domain.dto.user.response.user_output_dto import UserOutputDTO
from domain.entities.enums import CitizenshipEnum, GenderEnum, PositionEnum


class ContractorOutputDTO(UserOutputDTO):
    birthday: date
    height: int
    gender: GenderEnum
    citizenship: CitizenshipEnum
    positions: List[PositionEnum]

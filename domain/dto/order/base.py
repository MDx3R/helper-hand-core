from datetime import date, time
from typing import Optional
from domain.dto.base import ApplicationDTO
from domain.entities.enums import GenderEnum, PositionEnum


class OrderBaseDTO(ApplicationDTO):
    about: str
    address: str


class OrderDetailBaseDTO(ApplicationDTO):
    date: date
    start_at: time
    end_at: time
    position: PositionEnum
    gender: Optional[GenderEnum] = None
    count: int
    wager: int

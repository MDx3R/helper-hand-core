from datetime import date, time
from typing import Optional
import datetime

from pydantic import Field, field_validator
from domain.dto.base import ApplicationDTO
from domain.entities.enums import GenderEnum, PositionEnum


class OrderBaseDTO(ApplicationDTO):
    about: str = Field(..., min_length=1, max_length=1000)
    address: str = Field(..., min_length=1, max_length=255)


class OrderDetailBaseDTO(ApplicationDTO):
    date: date
    start_at: time
    end_at: time
    position: PositionEnum
    gender: Optional[GenderEnum] = None
    count: int = Field(..., ge=1, le=100)
    wager: int = Field(..., ge=0)

    @field_validator("date")
    @classmethod
    def validate_date_not_in_past(cls, v: datetime.date) -> datetime.date:
        if v < date.today():
            raise ValueError("date cannot be in the past")
        return v

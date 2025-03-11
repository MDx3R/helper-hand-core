from typing import List
from datetime import datetime

from .user_dto import UserOutputDTO

from domain.models import Contractee
from domain.models.enums import RoleEnum, GenderEnum, CitizenshipEnum, PositionEnum

class ContracteeOutputDTO(UserOutputDTO):
    """
    DTO выходных данных исполнителя.

    Этот класс используется для представления данных исполнителя на уровень представления.
    """

    birthday: datetime
    height: int
    gender: GenderEnum
    citizenship: CitizenshipEnum
    positions: List[PositionEnum]
    role: RoleEnum = RoleEnum.contractee

    @property
    def contractee_id(self) -> int:
        return self.user_id
    
    @classmethod
    def from_contractee(cls, contractee: Contractee) -> 'ContracteeOutputDTO':
        """
        Преобразует `Contractee` в `ContracteeOutputDTO`.
        """
        return cls(
            user_id=contractee.user_id,
            surname=contractee.surname,
            name=contractee.name,
            patronymic=contractee.patronymic,
            phone_number=contractee.phone_number,
            role=contractee.role,
            status=contractee.status,
            photos=contractee.photos,
            telegram_id=contractee.telegram_id,
            chat_id=contractee.chat_id,
            birthday=contractee.birthday,
            height=contractee.height,
            gender=contractee.gender,
            citizenship=contractee.citizenship,
            positions=contractee.positions
        )
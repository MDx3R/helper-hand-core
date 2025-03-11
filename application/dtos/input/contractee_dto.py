from typing import List
from datetime import datetime

from domain.models import Contractee 
from domain.models.enums import RoleEnum, GenderEnum, CitizenshipEnum, PositionEnum

from .user_dto import UserInputDTO

class ContracteeInputDTO(UserInputDTO):
    """
    DTO входных данных исполнителя.

    Этот класс используется для представления данных исполнителя, полученных из внешнего источника. 
    Он предназначен для валидации входных данных перед передачей в бизнес-логику.
    """

    birthday: datetime
    height: int
    gender: GenderEnum
    citizenship: CitizenshipEnum
    positions: List[PositionEnum]
    role: RoleEnum = RoleEnum.contractee

    def to_contractee(self) -> Contractee:
        """
        Преобразует `ContracteeInputDTO` в `Contractee`.
        
        Поле `status` устанавливается значением по умолчанию.
        Поле `role` устанавливается как `RoleEnum.contractee`.
        """
        return Contractee(
            surname=self.surname,
            name=self.name,
            patronymic=self.patronymic,
            phone_number=self.phone_number,
            role=RoleEnum.contractee,
            photos=self.photos,
            telegram_id=self.telegram_id,
            chat_id=self.chat_id,
            birthday=self.birthday,
            height=self.height,
            gender=self.gender,
            citizenship=self.citizenship,
            positions=self.positions
        )
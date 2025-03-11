from .user_dto import UserOutputDTO

from domain.models import Contractor
from domain.models.enums import RoleEnum

class ContractorOutputDTO(UserOutputDTO):
    """
    DTO выходных данных заказчика.

    Этот класс используется для представления данных заказчика на уровень представления.
    """

    about: str
    role: RoleEnum = RoleEnum.contractor
    
    @property
    def contractor_id(self) -> int:
        return self.user_id
    
    @classmethod
    def from_contractor(cls, contractor: Contractor) -> 'ContractorOutputDTO':
        """
        Преобразует `Contractor` в `ContractorOutputDTO`.
        """
        return cls(
            user_id=contractor.user_id,
            surname=contractor.surname,
            name=contractor.name,
            patronymic=contractor.patronymic,
            phone_number=contractor.phone_number,
            role=contractor.role,
            status=contractor.status,
            photos=contractor.photos,
            telegram_id=contractor.telegram_id,
            chat_id=contractor.chat_id,
            about=contractor.about
        )
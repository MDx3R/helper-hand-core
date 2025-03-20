from domain.entities import Contractor 
from domain.entities.enums import RoleEnum

from .user_dto import UserInputDTO

class ContractorInputDTO(UserInputDTO):
    """
    DTO входных данных заказчика.

    Этот класс используется для представления данных заказчика, полученных из внешнего источника. 
    Он предназначен для валидации входных данных перед передачей в бизнес-логику.
    """

    about: str
    role: RoleEnum = RoleEnum.contractor

    def to_contractor(self) -> Contractor:
        """
        Преобразует `ContractorInputDTO` в `Contractor`.
        
        Поле `status` устанавливается значением по умолчанию.
        Поле `role` устанавливается как `RoleEnum.contractor`.
        """
        return Contractor(
            surname=self.surname,
            name=self.name,
            patronymic=self.patronymic,
            phone_number=self.phone_number,
            role=RoleEnum.contractor,
            photos=self.photos,
            telegram_id=self.telegram_id,
            chat_id=self.chat_id,
            about=self.about
        )
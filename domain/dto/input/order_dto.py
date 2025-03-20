from typing import Optional
from pydantic import BaseModel

from domain.entities import Order 

class OrderInputDTO(BaseModel):
    """
    DTO входных данных заказа.

    Этот класс используется для представления данных заказа, полученных из внешнего источника. 
    Он предназначен для валидации входных данных перед передачей в бизнес-логику.
    """
    
    about: str
    address: str

    def to_order(self, contractor_id: int) -> Order:
        """
        Преобразует `OrderInputDTO` в `Order` с назначением `contractor_id`.
        
        Поле `status` устанавливается значением по умолчанию.
        """
        return Order(
            contractor_id=contractor_id,
            about=self.about,
            address=self.address,
        )
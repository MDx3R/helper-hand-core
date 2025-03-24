from typing import Optional
from pydantic import BaseModel

from domain.entities import Order 
from domain.entities.base import ApplicationModel

class OrderInputDTO(BaseModel):
    about: str
    address: str

    def to_order(self, contractor_id: int) -> Order:
        """
        Поле `status` устанавливается значением по умолчанию.
        """
        return Order.model_validate(self.model_dump() | {"contractor_id": contractor_id})
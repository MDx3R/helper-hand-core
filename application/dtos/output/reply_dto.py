from typing import Optional, List
from pydantic import BaseModel

from datetime import datetime

from domain.entities import Reply 
from domain.entities.enums import ReplyStatusEnum

class ReplyOutputDTO(BaseModel):
    """
    DTO выходных данных отклика на заказ.

    Этот класс используется для представления данных отклика на уровень представления.
    """

    contractee_id: int
    detail_id: int
    wager: Optional[int]
    status: ReplyStatusEnum
    paid: Optional[datetime]

    @classmethod
    def from_reply(cls, reply: Reply) -> 'ReplyOutputDTO':
        """
        Преобразует `Reply` в `ReplyOutputDTO`.
        """
        return cls(
            contractee_id=reply.contractee_id,
            detail_id=reply.detail_id,
            wager=reply.wager,
            status=reply.status,
            paid=reply.paid
        )
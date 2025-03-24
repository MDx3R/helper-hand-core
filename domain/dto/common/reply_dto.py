from typing import Optional, List
from pydantic import BaseModel

from datetime import datetime

from domain.entities import Reply 
from domain.entities.enums import ReplyStatusEnum
from domain.dto.base import ApplicationDTO

class ReplyDTO(ApplicationDTO):
    contractee_id: int
    detail_id: int
    wager: Optional[int]
    status: ReplyStatusEnum
    paid: Optional[datetime]

    @classmethod
    def from_reply(cls, reply: Reply) -> 'ReplyDTO':
        return cls.from_model(reply)
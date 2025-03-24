from pydantic import BaseModel

from domain.entities import Reply
from domain.entities.base import ApplicationModel

class ReplyInputDTO(BaseModel):
    detail_id: int
    contractee_id: int

    def to_reply(self, wager: int):
        """
        Поле `status` устанавливается значением по умолчанию.
        
        Args:
            wager (int): Ставка для исполнителя.
        """
        return Reply.model_validate(self.model_dump() | {"wager": wager})
from pydantic import BaseModel

from domain.entities import Reply

class ReplyInputDTO(BaseModel):
    """
    DTO входных данных откликов.

    Этот класс используется для создания отклика по данным, полученным из внешнего источника.
    """
    
    detail_id: int
    contractee_id: int

    def to_reply(self, wager: int):
        """
        Преобразует `ReplyInputDTO` в `Reply`.

        Поле `status` устанавливается значением по умолчанию.
        
        Args:
            wager (int): Ставка для исполнителя.
        """
        return Reply(
            detail_id=self.detail_id,
            contractee_id=self.contractee_id,
            wager=wager
        )
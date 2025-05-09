from typing import List
from domain.dto.order.internal.order_query_dto import (
    GetUserOrderAfterDTO,
    GetUserOrderDTO,
)
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderDetailOutputDTO,
)


# Administrative
# TODO: DTO с доступными позициями/Отправлять только доступные позиции
class GetSuitableOrderUseCase:
    # Заказ всегда подходит, если заказ открыт и подходят сведения -> GetSuitableDetailsUseCase
    async def execute(
        self, query: GetUserOrderAfterDTO
    ) -> CompleteOrderOutputDTO | None:
        pass


class GetSuitableDetailsUseCase:
    # Заказ открыт NOTE: Тут?
    # Есть места
    # Подходит по параметрам
    # Нет отклика на дату
    async def execute(
        self, query: GetUserOrderDTO
    ) -> List[OrderDetailOutputDTO]:
        pass

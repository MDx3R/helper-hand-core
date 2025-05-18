from application.usecases.order.order_query_use_case import ListOrdersUseCase
from domain.dto.base import SortingOrder
from domain.dto.order.internal.order_filter_dto import OrderFilterDTO
from domain.dto.user.internal.user_context_dto import PaginatedDTO


class ListParticipatedOrdersUseCase(ListOrdersUseCase):
    def _build_filter(self, query: PaginatedDTO) -> OrderFilterDTO:
        return OrderFilterDTO(
            contractee_id=query.context.user_id,
            last_id=query.last_id,
            size=query.size,
            sorting=SortingOrder.descending,
        )

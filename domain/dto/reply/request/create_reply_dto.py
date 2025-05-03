from domain.dto.order.internal.base import DetailIdDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO


class CreateReplyDTO(DetailIdDTO):
    detail_id: int
    context: UserContextDTO

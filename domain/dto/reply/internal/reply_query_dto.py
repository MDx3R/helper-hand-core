from domain.dto.base import PaginationDTO
from domain.dto.order.internal.base import DetailIdDTO, OrderIdDTO
from domain.dto.reply.internal.base import ReplyIdDTO
from domain.dto.user.internal.base import UserIdDTO
from domain.dto.user.internal.user_context_dto import WithUserContextDTO


class GetReplyDTO(ReplyIdDTO, WithUserContextDTO):
    pass


class GetContracteeRepliesDTO(UserIdDTO, PaginationDTO):
    pass


class GetOrderReplyDTO(OrderIdDTO, WithUserContextDTO):
    pass


class GetOrderRepliesDTO(GetOrderReplyDTO, PaginationDTO):
    pass


class GetDetailRepliesDTO(DetailIdDTO, WithUserContextDTO, PaginationDTO):
    pass

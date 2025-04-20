from domain.dto.base import InternalDTO


class ReplyIdDTO(InternalDTO):
    contractee_id: int
    detail_id: int

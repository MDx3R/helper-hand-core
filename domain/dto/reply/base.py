from domain.dto.base import ApplicationDTO


class ReplyBaseDTO(ApplicationDTO):
    contractee_id: int
    detail_id: int

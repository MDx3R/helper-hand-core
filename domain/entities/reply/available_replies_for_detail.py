from domain.entities.base import ApplicationModel


class AvailableRepliesForDetail(ApplicationModel):
    detail_id: int
    quantity: int
    """Количество свободных мест на позицию."""

from .base import ApplicationModel

class AvailableRepliesForDetail(ApplicationModel):
    detail_id: int
    """Идентификатор позиции."""

    quantity: int
    """Количество свободных мест на позицию."""

    def is_full(self) -> bool:
        return self.quantity <= 0
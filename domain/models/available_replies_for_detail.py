from .base import ApplicationModel

class AvailableRepliesForDetail(ApplicationModel):
    detail_id: int
    quantity: int

    def is_full(self) -> bool:
        return self.quantity <= 0
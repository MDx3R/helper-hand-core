from domain.exceptions.base import ServiceException

class NotFoundException(ServiceException):
    """Объект не найден"""
    def __init__(self, entity_id: int = None):
        self.entity_id = entity_id

        if entity_id is None:
            super().__init__("Объект не найден")
        else:
            super().__init__(f"Объект (id={entity_id}) не найден")
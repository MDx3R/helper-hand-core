from domain.exceptions.base import ServiceException

class InvalidInput(ServiceException):
    """Некорректный ввод"""
    def __init__(self, message: str = "Некорректный ввод."):
        super().__init__(message)
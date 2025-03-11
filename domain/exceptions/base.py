class ApplicationException(Exception):
    """Базовое исключение для всего приложения"""
    def __init__(self, message: str = None):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message or self.__class__.__name__
    
class RepositoryException(ApplicationException):
    """
    Базовое исключение для ошибок репозитория.
    
    Возникают при ошибках в работе репозиториев.
    """

class DatabaseException(RepositoryException):
    """
    Базовое исключение для ошибок базы данных.
    
    Возникают при ошибках в работе репозиториев.
    """

class ServiceException(ApplicationException):
    """Базовое исключение для ошибок бизнес-логики"""
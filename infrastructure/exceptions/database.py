from domain.exceptions.base import DatabaseException

class TransactionException(DatabaseException):
    """Ошибка при выполнении транзакции."""
    def __init__(self, message: str = "Транзакция не была выполнена"):
        super().__init__(message)

class DatabaseUnavailableException(DatabaseException):
    """Ошибка соединения с базой данных."""
    def __init__(self, message: str = "База данных недоступна"):
        super().__init__(message)

class InvalidQueryException(DatabaseException):
    """Ошибка в SQL-запросе."""
    def __init__(self, message: str = "Некорректный SQL-запрос"):
        super().__init__(message)

class InvalidDataException(DatabaseException):
    """Ошибка некорректных данных."""
    def __init__(self, message: str = "Некорректные данные в запросе"):
        super().__init__(message)

class InvalidStatementException(DatabaseException):
    """Ошибка в параметрах SQL-запроса."""
    def __init__(self, message: str = "Ошибка в параметрах SQL-запроса"):
        super().__init__(message)
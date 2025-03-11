from domain.exceptions.base import RepositoryException

class IntegrityException(RepositoryException):
    """
    Нарушение целостности данных. 
    
    Возникают при использовании некорректных или недостающих данных.
    """
    def __init__(self, message: str = "Нарушение целостности данных"):
        super().__init__(message)

class DuplicateEntryException(RepositoryException):
    """
    Конфликт уникальности поля
    
    Возникает при попытке преодолеть ограничение уникальности.
    """
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(
            f"Дублирующая запись для поля '{field}': {value} уже существует"
        )
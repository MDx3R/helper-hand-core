from domain.exceptions.base import ServiceException

class PermissionDeniedException(ServiceException):
    """Вызывается при попытке выполнения действия без необходимых прав."""
    def __init__(self, action: str, user_id: int = None):
        self.action = action
        self.user_id = user_id

        message = f"Отказано в доступе '{action}'"
        if user_id:
            message += f" (user_id={user_id})"
            
        super().__init__(message)

class AlreadyAuthenticatedException(ServiceException):
    """Ошибка, возникающая при попытке прохождения повторной регистрации или авторизации пользователем."""
    def __init__(self, message: str = "Пользователь уже зарегистрирован."):
        super().__init__(message)

class UserBlockedException(ServiceException):
    """Ошибка, возникающая при попытке выполнения действия заблокированным пользователем."""
    def __init__(self, message: str = "Пользователь заблокирован."):
        super().__init__(message)

class UnauthorizedAccessException(ServiceException):
    """Ошибка, возникающая при попытке выполнения действия без авторизации."""
    def __init__(self, message: str = "Доступ запрещен. Пользователь не авторизован."):
        super().__init__(message)
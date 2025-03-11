from domain.exceptions.base import ServiceException

class UserStatusChangeNotAllowedException(ServiceException):
    """Вызывается при попытке изменить статус пользователя в конкретном состоянии на недопустимый."""
    def __init__(self, user_id: int, status: str, comment: str | None = None):
        self.user_id = user_id
        self.status = status
        self.comment = comment

        message = f"Невозможно изменить статус пользователя (id={user_id}) на '{status}'"
        if comment:
            message += f": {comment}"

        super().__init__(message)
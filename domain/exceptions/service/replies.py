from domain.exceptions.base import ServiceException

class InvalidReplyException(ServiceException):
    """
    Вызывается при попытке отправить недопустимый отклик.
    
    Причины:
      - Заказ неактивен.
      - Отклик уже был отправлен ранее.
      - Указанная дата недоступна (прошла или занята другим откликом).
    """
    def __init__(self, message: str = "Отклик не может быть отправлен"):
        super().__init__(message)

class DetailFullException(ServiceException):
    """
    Вызывается при попытке подтвердить или отправить отклик на заказ, который уже имеет максимальное допустимое количество подтверждённых откликов.
    """
    def __init__(self, message: str = "Достигнуто максимальное количество откликов на заказ"):
        super().__init__(message)

class ReplyStatusChangeNotAllowedException(ServiceException):
    """Вызывается, когда действие недоступно из-за текущего статуса отклика."""
    def __init__(self, contractee_id: int, detail_id: int, status: str, action: str):
        self.contractee_id = contractee_id
        self.detail_id = detail_id
        self.status = status
        self.action = action

        message = f"Невозможно выполнить действие '{action}' для отклика (contractee_id={contractee_id}, detail_id={detail_id}) со статусом '{status}'"
        super().__init__(message)

class ReplySubmitNotAllowedException(ServiceException):
    """
    Вызывается при отправить отклик на недопустимую позицию или заказ.
    """
    def __init__(self, message: str = "Отклик не может быть отправлен"):
        super().__init__(message)
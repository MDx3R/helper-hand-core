from domain.dto.base import ApplicationDTO

class NotificationDTO(ApplicationDTO):
    pass

class ReceiverNotificationDTO(NotificationDTO):
    """Базовый класс для DTO уведомлений пользователя"""
    receiver_id: int

class ExecutorNotificationDTO(NotificationDTO):
    """Базовый класс для DTO уведомлений с указанием исполнителя"""
    executor_id: int

class NotificationContextDTO(NotificationDTO):
    """Базовый класс для контекста DTO уведомлений"""
    context: str = ""
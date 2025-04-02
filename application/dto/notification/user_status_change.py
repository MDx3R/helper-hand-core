from .base import ReceiverNotificationDTO, ExecutorNotificationDTO, NotificationMessageDTO

class UserStatusChangeNotificationDTO(
    ReceiverNotificationDTO,
    ExecutorNotificationDTO,
    NotificationMessageDTO
):
    pass

class RegistrationApprovedNotificationDTO(UserStatusChangeNotificationDTO):
    pass

class RegistrationDisapprovedNotificationDTO(UserStatusChangeNotificationDTO):
    pass

class UserDroppedNotificationDTO(UserStatusChangeNotificationDTO):
    pass

class UserBannedNotificationDTO(UserStatusChangeNotificationDTO):
    pass
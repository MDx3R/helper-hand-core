from .base import ReceiverNotificationDTO, ExecutorNotificationDTO, NotificationContextDTO

class UserStatusChangeNotificationDTO(
    ReceiverNotificationDTO,
    ExecutorNotificationDTO,
    NotificationContextDTO
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
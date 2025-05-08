from .base import NotificationDTO


class NewOrderNotificationDTO(NotificationDTO):
    pass


class AdminAssignedNotificationDTO(NotificationDTO):
    pass


class OrderApprovedNotificationDTO(NotificationDTO):
    pass


class OrderDisapprovedNotificationDTO(NotificationDTO):
    pass


class OrderClosedNotificationDTO(NotificationDTO):
    pass


class OrderOpenedNotificationDTO(NotificationDTO):
    pass


class OrderSetActiveNotificationDTO(NotificationDTO):
    pass


class OrderCancelledNotificationDTO(NotificationDTO):
    pass


class OrderFulfilledNotificationDTO(NotificationDTO):
    pass

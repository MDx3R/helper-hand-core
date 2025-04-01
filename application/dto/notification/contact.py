from .base import ReceiverNotificationDTO, ExecutorNotificationDTO, NotificationContextDTO

class ContactNotificationDTO(
    ReceiverNotificationDTO, 
    ExecutorNotificationDTO, 
    NotificationContextDTO
):
    pass

class AdminContactNotificationDTO(ContactNotificationDTO):
    pass

class ContracteeContactNotificationDTO(ContactNotificationDTO):
    pass

class ContractorContactNotificationDTO(ContactNotificationDTO):
    pass
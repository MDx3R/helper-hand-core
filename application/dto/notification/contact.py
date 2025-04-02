from .base import ReceiverNotificationDTO, ExecutorNotificationDTO, NotificationMessageDTO

class ContactNotificationDTO(
    ReceiverNotificationDTO, 
    ExecutorNotificationDTO, 
    NotificationMessageDTO
):
    pass

class AdminContactNotificationDTO(ContactNotificationDTO):
    pass

class ContracteeContactNotificationDTO(ContactNotificationDTO):
    pass

class ContractorContactNotificationDTO(ContactNotificationDTO):
    pass
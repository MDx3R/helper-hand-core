from abc import ABC, abstractmethod

from application.dto.notification import (
    RegistrationApprovedNotificationDTO,
    RegistrationDisapprovedNotificationDTO,
    UserDroppedNotificationDTO,
    UserBannedNotificationDTO
)
from application.dto.notification import AdminContactNotificationDTO

class UserNotificationService(ABC):
    @abstractmethod
    async def send_registration_approved_notification(
        self, 
        context: RegistrationApprovedNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_registration_disapproved_notification(
        self, 
        context: RegistrationDisapprovedNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_admin_contact_notification(
        self, 
        context: AdminContactNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_user_dropped_notification(
        self, 
        context: UserDroppedNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_user_banned_notification(
        self, 
        context: UserBannedNotificationDTO
    ):
        pass
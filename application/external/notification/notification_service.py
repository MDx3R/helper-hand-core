from abc import ABC, abstractmethod

from domain.entities import User, Admin

class NotificationService(ABC):
    async def send_registration_approved_notification(self, user: User):
        pass

    async def send_registration_disapproved_notification(self, user: User):
        pass

    async def send_admin_contact_notification(self, user: User, admin: Admin):
        pass

    async def send_user_dropped_notification(self, user: User):
        pass

    async def send_user_banned_notification(self, user: User):
        pass
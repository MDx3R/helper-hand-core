from abc import ABC, abstractmethod

from application.dto.notification import (
    RegistrationApprovedNotificationDTO,
    RegistrationDisapprovedNotificationDTO,
    UserDroppedNotificationDTO,
    UserBannedNotificationDTO,
)
from application.dto.notification import AdminContactNotificationDTO
from application.dto.notification import (
    NewOrderNotificationDTO,
    AdminAssignedNotificationDTO,
    OrderApprovedNotificationDTO,
    OrderDisapprovedNotificationDTO,
    OrderClosedNotificationDTO,
    OrderOpenedNotificationDTO,
    OrderSetActiveNotificationDTO,
    OrderCancelledNotificationDTO,
    OrderFulfilledNotificationDTO,
    NewReplyNotificationDTO,
    ReplyApprovedNotificationDTO,
    ReplyDisapprovedNotificationDTO,
)  # TODO: Объявить


class UserNotificationService(ABC):
    @abstractmethod
    async def send_registration_approved_notification(
        self, context: RegistrationApprovedNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_registration_disapproved_notification(
        self, context: RegistrationDisapprovedNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_admin_contact_notification(
        self, context: AdminContactNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_user_dropped_notification(
        self, context: UserDroppedNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_user_banned_notification(
        self, context: UserBannedNotificationDTO
    ):
        pass


class AdminOrderNotificationService(ABC):
    @abstractmethod
    async def send_new_order_notification(
        self, context: NewOrderNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_order_cancelled_notification(
        self, context: OrderCancelledNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_order_set_active_notification(
        self, context: OrderSetActiveNotificationDTO
    ):
        pass


class ContracteeOrderNotificationService(ABC):
    @abstractmethod
    async def send_new_order_notification(
        self, context: NewOrderNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_order_set_active_notification(
        self, context: OrderSetActiveNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_order_cancelled_notification(
        self, context: OrderCancelledNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_order_fulfilled_notification(
        self, context: OrderFulfilledNotificationDTO
    ):
        pass


class ContractorOrderNotificationService(ABC):
    @abstractmethod
    async def send_admin_assigned_notification(
        self, context: AdminAssignedNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_order_approved_notification(
        self, context: OrderApprovedNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_order_disapproved_notification(
        self, context: OrderDisapprovedNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_order_closed_notification(
        self, context: OrderClosedNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_order_opened_notification(
        self, context: OrderOpenedNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_order_cancelled_notification(
        self, context: OrderCancelledNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_order_fulfilled_notification(
        self, context: OrderFulfilledNotificationDTO
    ):
        pass


class ContracteeReplyNotificationService(ABC):
    @abstractmethod
    async def send_reply_approved_notification(
        self, context: ReplyApprovedNotificationDTO
    ):
        pass

    @abstractmethod
    async def send_reply_disapproved_notification(
        self, context: ReplyDisapprovedNotificationDTO
    ):
        pass


class ContractorReplyNotificationService(ABC):
    @abstractmethod
    async def send_new_reply_notification(
        self, context: NewReplyNotificationDTO
    ):
        pass

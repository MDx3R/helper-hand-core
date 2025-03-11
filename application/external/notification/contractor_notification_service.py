from abc import ABC, abstractmethod

from domain.models import Contractor, Order

class ContractorNotificationService(ABC):
    @abstractmethod
    async def send_admin_assigned_for_order_notification(self, contractor: Contractor, order: Order):
        pass

    @abstractmethod
    async def send_order_approved_notification(self, contractor: Contractor, order: Order):
        pass

    @abstractmethod
    async def send_order_closed_notification(self, contractor: Contractor, order: Order):
        pass

    @abstractmethod
    async def send_order_opened_notification(self, contractor: Contractor, order: Order):
        pass

    @abstractmethod
    async def send_order_cancelled_notification(self, contractor: Contractor, order: Order):
        pass

    @abstractmethod
    async def send_order_fulfilled_notification(self, contractor: Contractor, order: Order):
        pass

    @abstractmethod
    async def send_new_reply_notification(self, contractor: Contractor):
        pass

    @abstractmethod
    async def send_order_closed_automatically_notification(self, contractor: Contractor, order: Order):
        pass
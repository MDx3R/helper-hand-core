from typing import List
from abc import ABC, abstractmethod

from domain.models import Contractee, DetailedReply, Order, OrderDetail

class ContracteeNotificationService(ABC):
    @abstractmethod
    async def send_new_order_notification(self, contractee: Contractee, order: Order):
        pass

    @abstractmethod
    async def send_order_set_active_notification(self, contractee: Contractee, order: Order):
        pass

    @abstractmethod
    async def send_order_cancelled_notification(self, contractee: Contractee, order: Order):
        pass

    @abstractmethod
    async def send_reply_approved_notification(self, contractee: Contractee, order: Order, detail: OrderDetail):
        pass

    @abstractmethod
    async def send_reply_disapproved_notification(self, contractee: Contractee, order: Order, detail: OrderDetail):
        pass

    @abstractmethod
    async def send_order_detail_full_notification_many(self, contractees: List[Contractee], order: Order, detail: OrderDetail):
        pass

    @abstractmethod
    async def send_order_full_notification_many(self, contractees: List[Contractee], order: Order):
        pass

    @abstractmethod
    async def send_order_set_active_notification_many(self, contractees: List[Contractee], order: Order):
        pass

    @abstractmethod
    async def send_order_cancelled_notification_many(self, contractees: List[Contractee], order: Order):
        pass

    @abstractmethod
    async def send_reply_disapproved_notification_many(self, contractees: List[Contractee], order: Order):
        pass
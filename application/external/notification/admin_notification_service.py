from typing import List
from abc import ABC, abstractmethod

from domain.entities import Admin, Contractor, Contractee, Order, OrderDetail, DetailedOrder
from domain.repositories import UserRepository

class AdminNotificationService(ABC):
    @abstractmethod
    async def send_new_registration_notification(self):
        pass

    @abstractmethod
    async def send_new_order_notification(self):
        pass

    @abstractmethod
    async def send_order_cancelled_notification(self, order: Order):
        pass

    @abstractmethod
    async def send_order_set_active_notification(self, order: Order):
        pass

    @abstractmethod
    async def send_order_closed_automatically_notification(self, order: Order):
        pass
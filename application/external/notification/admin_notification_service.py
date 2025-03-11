from typing import List
from abc import ABC, abstractmethod

from domain.models import Admin, Contractor, Contractee, Order, OrderDetail, DetailedOrder
from domain.repositories import UserRepository

class AdminNotificationService(ABC):
    @abstractmethod
    async def send_new_contractor_registration_notification(self, admins: List[Admin], contractor: Contractor):
        pass

    @abstractmethod
    async def send_new_contractee_registration_notification(self, admins: List[Admin], contractee: Contractee):
        pass
    
    @abstractmethod
    async def send_new_order_notification(self, admins: List[Admin], order: Order, details: List[OrderDetail]):
        pass

    @abstractmethod
    async def send_order_cancelled_notification(self, admin: Admin, order: Order):
        pass

    @abstractmethod
    async def send_order_set_active_notification(self, admin: Admin, order: Order):
        pass

    @abstractmethod
    async def send_order_closed_automatically_notification(self, admin: Admin, order: Order):
        pass
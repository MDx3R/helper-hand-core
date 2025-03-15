from typing import overload, List, Union

from domain.models import Order, OrderDetail, Admin, Contractee, AvailableRepliesForDetail
from domain.models.enums import OrderStatusEnum, GenderEnum

from domain.time import is_current_time_valid_for_reply

class AdminDomainService:
    @staticmethod
    def is_contractor(admin: Admin) -> bool:
        return admin.contractor_id is not None

class OrderDomainService:
    @staticmethod
    def is_owned_by(order: Order, contractor_id: int) -> bool:
        return contractor_id == order.contractor_id
    
    @staticmethod
    def is_supervised_by(order: Order, user_id: int) -> bool:
        return user_id == order.supervisor_id
    
    @staticmethod
    def has_supervisor(order: Order) -> bool:
        return order.supervisor_id is not None

    @staticmethod
    def is_available(order: Order) -> bool:
        return order.status == OrderStatusEnum.open

    @staticmethod
    def can_be_assigned(order: Order) -> bool:
        return order.supervisor_id is None and order.status == OrderStatusEnum.created

    @staticmethod
    def can_be_approved(order: Order) -> bool:
        return order.status == OrderStatusEnum.created

    @staticmethod
    def can_be_cancelled(order: Order) -> bool:
        return order.status != OrderStatusEnum.fulfilled and order.status != OrderStatusEnum.cancelled
    
    @staticmethod
    def can_be_closed(order: Order) -> bool:
        return order.status == OrderStatusEnum.open
    
    @staticmethod
    def can_be_opened(order: Order) -> bool:
        return order.status == OrderStatusEnum.closed
    
    @staticmethod
    def can_be_fulfilled(order: Order) -> bool:
        return order.status == OrderStatusEnum.closed
    
class OrderDetailDomainService:
    @staticmethod
    def is_suitable(detail: OrderDetail, contractee: Contractee) -> bool:
        return not detail.gender or detail.gender == contractee.gender
    
    @staticmethod
    def is_relevant_at_current_time(detail: OrderDetail) -> bool:
        return is_current_time_valid_for_reply(detail.date)
    
class AvailabilityDomainService:
    @staticmethod
    def is_full(availability: AvailableRepliesForDetail) -> bool:
        return availability.quantity <= 0
    
    @staticmethod
    def are_all_full(availabilities: List[AvailableRepliesForDetail]) -> bool:
        return all(AvailabilityDomainService.is_full(av) for av in availabilities)
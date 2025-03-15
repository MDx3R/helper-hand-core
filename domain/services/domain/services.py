from typing import overload, List, Union

from domain.models import Order, OrderDetail, Reply, User, Admin, Contractee, AvailableRepliesForDetail
from domain.models.enums import RoleEnum, UserStatusEnum, OrderStatusEnum, GenderEnum, ReplyStatusEnum

from domain.time import is_current_time_valid_for_reply

class UserDomainService:
    @staticmethod
    def is_pending(user: User) -> bool:
        return user.status == UserStatusEnum.pending
    
    @staticmethod
    def is_registered(user: User) -> bool:
        return user.status == UserStatusEnum.registered
    
    @staticmethod
    def is_dropped(user: User) -> bool:
        return user.status == UserStatusEnum.dropped
    
    @staticmethod
    def is_banned(user: User) -> bool:
        return user.status == UserStatusEnum.banned

    @staticmethod
    def is_contractee(user: User) -> bool:
        return user.role == RoleEnum.contractee 

    @staticmethod
    def is_contractor(user: User) -> bool:
        return user.role == RoleEnum.contractor 
    
    @staticmethod
    def is_admin(user: User) -> bool:
        return user.role == RoleEnum.admin 

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
    def is_created(order: Order) -> bool:
        return order.status == OrderStatusEnum.created

    @staticmethod
    def is_open(order: Order) -> bool:
        return order.status == OrderStatusEnum.open
    
    @staticmethod
    def is_closed(order: Order) -> bool:
        return order.status == OrderStatusEnum.closed

    @staticmethod
    def is_active(order: Order) -> bool:
        return order.status == OrderStatusEnum.active

    @staticmethod
    def is_cancelled(order: Order) -> bool:
        return order.status == OrderStatusEnum.cancelled

    @staticmethod
    def is_fulfilled(order: Order) -> bool:
        return order.status == OrderStatusEnum.fulfilled

    @classmethod
    def is_available(cls, order: Order) -> bool:
        return cls.is_open(order)

    @classmethod
    def can_be_assigned(cls, order: Order) -> bool:
        return not cls.has_supervisor(order) and cls.is_created(order)

    @classmethod
    def can_be_approved(cls, order: Order) -> bool:
        return cls.is_created(order)

    @classmethod
    def can_be_cancelled(cls, order: Order) -> bool:
        return not cls.is_fulfilled(order) and not cls.is_cancelled(order)
    
    @classmethod
    def can_be_closed(cls, order: Order) -> bool:
        return cls.is_open(order)
    
    @classmethod
    def can_be_opened(cls, order: Order) -> bool:
        return cls.is_closed(order)
    
    @classmethod
    def can_be_set_active(cls, order: Order) -> bool:
        return cls.is_open(order) or cls.is_closed(order)

    @classmethod
    def can_be_fulfilled(cls, order: Order) -> bool:
        return cls.is_active(order)
    
    @classmethod
    def can_have_replies(cls, order: Order) -> bool:
        return cls.is_open(order)
    
class OrderDetailDomainService:
    @staticmethod
    def is_suitable(detail: OrderDetail, contractee: Contractee) -> bool:
        return not detail.gender or detail.gender == contractee.gender
    
    @staticmethod
    def is_relevant_at_current_time(detail: OrderDetail) -> bool:
        return is_current_time_valid_for_reply(detail.date)
    
class ReplyDomainService:
    @staticmethod
    def is_created(reply: Reply) -> bool:
        return reply.status == ReplyStatusEnum.created

    @staticmethod
    def is_accepted(reply: Reply) -> bool:
        return reply.status == ReplyStatusEnum.accepted
    
    @staticmethod
    def is_dropped(reply: Reply) -> bool:
        return reply.status == ReplyStatusEnum.dropped
    
    @staticmethod
    def is_paid(reply: Reply) -> bool:
        return reply.status == ReplyStatusEnum.paid
    
    @classmethod
    def can_be_approved(cls, reply: Reply) -> bool:
        return cls.is_created(reply)
    
    @classmethod
    def can_be_dropped(cls, reply: Reply) -> bool:
        return cls.is_created(reply)

class AvailabilityDomainService:
    @staticmethod
    def is_full(availability: AvailableRepliesForDetail) -> bool:
        return availability.quantity <= 0
    
    @classmethod
    def are_all_full(cls, availabilities: List[AvailableRepliesForDetail]) -> bool:
        return all(cls.is_full(av) for av in availabilities)
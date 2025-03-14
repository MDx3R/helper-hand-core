from domain.models import Order, Admin
from domain.models.enums import OrderStatusEnum

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
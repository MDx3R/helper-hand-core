from domain.dto.order.internal.base import OrderIdDTO
from domain.entities.order.enums import OrderStatusEnum


class SetOrderStatusDTO(OrderIdDTO):
    status: OrderStatusEnum


class SetOrderAdminDTO(OrderIdDTO):
    admin_id: int

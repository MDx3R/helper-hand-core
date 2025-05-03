from domain.dto.order.internal.base import OrderIdDTO
from domain.dto.user.internal.user_context_dto import WithUserContextDTO


class OrderManagementDTO(OrderIdDTO, WithUserContextDTO):
    pass


class SetOrderActiveDTO(OrderManagementDTO):
    pass


class TakeOrderDTO(OrderManagementDTO):
    pass


class ApproveOrderDTO(OrderManagementDTO):
    pass


class DisapproveOrderDTO(ApproveOrderDTO):
    pass


class CancelOrderDTO(OrderManagementDTO):
    pass


class CloseOrderDTO(OrderManagementDTO):
    pass


class OpenOrderDTO(OrderManagementDTO):
    pass


class FulfillOrderDTO(OrderManagementDTO):
    pass

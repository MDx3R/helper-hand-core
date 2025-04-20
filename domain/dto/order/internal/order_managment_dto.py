from domain.dto.order.internal.base import OrderIdDTO, OrderWithUserContextDTO


class OrderManagementDTO(OrderIdDTO, OrderWithUserContextDTO):
    pass


class SetOrderActiveDTO(OrderManagementDTO):
    pass


class TakeOrderDTO(OrderManagementDTO):
    pass


class ApproveOrderDTO(OrderManagementDTO):
    pass


class DisapproveOrderDTO(OrderManagementDTO):
    pass


class CancelOrderDTO(OrderManagementDTO):
    pass


class CloseOrderDTO(OrderManagementDTO):
    pass


class OpenOrderDTO(OrderManagementDTO):
    pass


class FulfillOrderDTO(OrderManagementDTO):
    pass

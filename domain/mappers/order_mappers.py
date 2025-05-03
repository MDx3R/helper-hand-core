from domain.dto.order.request.order_input_dto import (
    OrderDetailInputDTO,
    OrderInputDTO,
)
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderDetailOutputDTO,
    OrderOutputDTO,
    OrderWithDetailsOutputDTO,
)
from domain.entities.order.composite_order import (
    CompleteOrder,
    OrderWithDetails,
)
from domain.entities.order.detail import OrderDetail
from domain.entities.order.order import Order
from domain.mappers.base import from_entity_to_dto, from_dto_to_entity


class OrderMapper:
    @staticmethod
    def to_output(order: Order) -> OrderOutputDTO:
        return from_entity_to_dto(order, OrderOutputDTO)

    @staticmethod
    def to_output_with_details(
        order: OrderWithDetails,
    ) -> OrderWithDetailsOutputDTO:
        return from_entity_to_dto(order, OrderWithDetailsOutputDTO)

    @staticmethod
    def to_complete(order: CompleteOrder) -> CompleteOrderOutputDTO:
        return from_entity_to_dto(order, CompleteOrderOutputDTO)

    @staticmethod
    def from_input(order: OrderInputDTO, contractor_id: int) -> Order:
        return from_dto_to_entity(order, Order, contractor_id=contractor_id)


class OrderDetailMapper:
    @staticmethod
    def to_output(detail: OrderDetail) -> OrderDetailOutputDTO:
        return from_entity_to_dto(detail, OrderDetailOutputDTO)

    @staticmethod
    def from_input(
        order: OrderDetailInputDTO, order_id: int, fee: int
    ) -> OrderDetail:
        return from_dto_to_entity(
            order, OrderDetail, order_id=order_id, fee=fee
        )

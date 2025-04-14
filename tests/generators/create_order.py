from domain.dto.common import UserDTO
from domain.dto.common.detailed_order_dto import DetailedOrderDTO
from domain.dto.input.order_detail_dto import OrderDetailInputDTO
from domain.dto.input.order_dto import OrderInputDTO
from domain.dto.input.registration import UserRegistrationDTO
from domain.entities.enums import OrderStatusEnum
from domain.entities.order import Order
from domain.entities.order_detail import OrderDetail
from tests.factories import OrderDetailFactory, OrderFactory
from tests.generators.base import TestCaseGenerator

from .test_cases import CreateOrderTestCase


class CreateOrderTestCaseGenerator(TestCaseGenerator[CreateOrderTestCase]):
    presets = {"default": {"status": OrderStatusEnum.created}}

    @classmethod
    def _create_test_case(cls, **kwargs) -> CreateOrderTestCase:
        order = cls._get_random_order_data(**kwargs)
        details = cls._get_random_details_data(**kwargs)

        return cls._build_test_case(order, details)

    @classmethod
    def _get_random_order_data(cls, **kwargs):
        return OrderFactory.get_random_data(**kwargs)

    @classmethod
    def _get_random_details_data(cls, **kwargs):
        return [OrderDetailFactory.get_random_data(**kwargs) for _ in range(5)]

    @classmethod
    def _build_test_case(cls, order, details) -> CreateOrderTestCase:
        return CreateOrderTestCase(
            cls._build_order_input(order),
            cls._build_details_input(details),
            cls._build_output(order, details),
        )

    @classmethod
    def _build_order_input(cls, data) -> UserRegistrationDTO:
        return OrderInputDTO.model_validate(data)

    @classmethod
    def _build_details_input(cls, data) -> UserRegistrationDTO:
        return [OrderDetailInputDTO.model_validate(d) for d in data]

    @classmethod
    def _build_output(
        cls,
        order_input,
        details_input,
    ) -> UserDTO:
        order = Order.model_validate(order_input)
        counter = 1
        details = []
        for d in details_input:
            details.append(
                OrderDetail.model_validate(
                    d | {"detail_id": counter, "order_id": order.order_id}
                )
            )
            counter += 1

        return DetailedOrderDTO.from_order_and_details(order, details)

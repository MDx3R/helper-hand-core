import pytest

from application.usecases.order import (
    CreateAdminOrderUseCase,
    CreateOrderDetailsUseCase,
    CreateOrderUseCase,
)
from domain.dto.common import DetailedOrderDTO
from domain.dto.internal import CreateOrderDTO
from domain.repositories import OrderDetailRepository, OrderRepository
from domain.wager import calculate_pay
from tests.generators.create_order import CreateOrderTestCaseGenerator

from .conftest import create_context, set_up_counter


@pytest.fixture
def create_details_use_case(order_detail_repository):
    return CreateOrderDetailsUseCase(order_detail_repository)


class TestCreateOrderUseCase:
    @pytest.fixture
    def use_case(self, order_repository, create_details_use_case):
        return CreateOrderUseCase(order_repository, create_details_use_case)

    @pytest.mark.asyncio
    async def test_create_order_success(
        self,
        use_case: CreateOrderUseCase,
        order_repository: OrderRepository,
        order_detail_repository: OrderDetailRepository,
    ):
        # Arrange
        context = create_context()
        test_case = CreateOrderTestCaseGenerator.create(
            contractor_id=context.user_id, admin_id=None
        )
        order, details, expected = (
            test_case.order,
            test_case.details,
            test_case.expected,
        )

        set_up_counter(expected.order_id)

        # Act
        result = await use_case.create_order(
            CreateOrderDTO(
                order=order,
                details=details,
                context=context,
            )
        )

        # Assert
        assert isinstance(result, DetailedOrderDTO)
        assert result == expected

        order_repository.save.assert_awaited_once_with(
            order.to_order(context.user_id)
        )
        order_detail_repository.create_details.assert_awaited_once_with(
            [
                d.to_order_detail(
                    expected.order_id, d.wager - calculate_pay(d.wager)
                )
                for d in details
            ]
        )


class TestCreateAdminOrderUseCase:
    @pytest.fixture
    def use_case(self, order_repository, create_details_use_case):
        return CreateAdminOrderUseCase(
            order_repository, create_details_use_case
        )

    @pytest.mark.asyncio
    async def test_create_admin_order_success(
        self,
        use_case: CreateAdminOrderUseCase,
        order_repository: OrderRepository,
        order_detail_repository: OrderDetailRepository,
    ):
        # Arrange
        context = create_context()
        test_case = CreateOrderTestCaseGenerator.create(
            contractor_id=context.user_id, admin_id=context.user_id
        )
        order, details, expected = (
            test_case.order,
            test_case.details,
            test_case.expected,
        )

        set_up_counter(expected.order_id)

        # Act
        result = await use_case.create_order(
            CreateOrderDTO(
                order=order,
                details=details,
                context=context,
            )
        )

        # Assert
        assert isinstance(result, DetailedOrderDTO)
        assert result == expected

        passed_order = order.to_order(context.user_id)
        passed_order.admin_id = context.user_id
        order_repository.save.assert_awaited_once_with(passed_order)
        order_detail_repository.create_details.assert_awaited_once_with(
            [
                d.to_order_detail(
                    expected.order_id, d.wager - calculate_pay(d.wager)
                )
                for d in details
            ]
        )

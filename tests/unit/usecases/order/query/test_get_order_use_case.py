import pytest

from application.usecases.order import (
    GetDetailedOrderUseCase,
    GetOrderUseCase,
    GetOrderUseCaseFacade,
)
from domain.dto.common import DetailedOrderDTO, OrderDTO
from domain.dto.internal import GetOrderDTO
from domain.entities import DetailedOrder, Order
from domain.repositories import OrderRepository

from .conftest import (
    get_detailed_order_test_data,
    get_order_test_data,
    setup_repository,
)


class TestGetOrderUseCase:
    @pytest.fixture
    def use_case(self, order_repository):
        return GetOrderUseCaseFacade(order_repository)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("order, expected", get_order_test_data)
    async def test_get_order_success(
        self,
        use_case: GetOrderUseCase,
        order_repository: OrderRepository,
        order: Order,
        expected: OrderDTO,
    ):
        setup_repository(order_repository, order)

        result = await use_case.get_order(GetOrderDTO(order_id=order.order_id))

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_order_not_found(
        self,
        use_case: GetOrderUseCase,
        order_repository: OrderRepository,
    ):
        setup_repository(order_repository, None)

        result = await use_case.get_order(GetOrderDTO(order_id=999))

        assert result is None

        order_repository.get_order.assert_awaited_once_with(999)

    @pytest.mark.asyncio
    async def test_get_order_is_called(
        self,
        use_case: GetOrderUseCase,
        order_repository: OrderRepository,
    ):
        await use_case.get_order(GetOrderDTO(order_id=1))

        order_repository.get_order.assert_awaited_once_with(1)


class TestGetDetailedOrderUseCase:
    @pytest.fixture
    def use_case(self, order_repository):
        return GetOrderUseCaseFacade(order_repository)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("order, expected", get_detailed_order_test_data)
    async def test_get_detailed_order_success(
        self,
        use_case: GetDetailedOrderUseCase,
        order_repository: OrderRepository,
        order: DetailedOrder,
        expected: DetailedOrderDTO,
    ):
        setup_repository(order_repository, order)

        result = await use_case.get_detailed_order(
            GetOrderDTO(order_id=order.order_id)
        )

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_detailed_order_not_found(
        self,
        use_case: GetDetailedOrderUseCase,
        order_repository: OrderRepository,
    ):
        setup_repository(order_repository, None)

        result = await use_case.get_detailed_order(GetOrderDTO(order_id=999))

        assert result is None

        order_repository.get_detailed_order.assert_awaited_once_with(999)

    @pytest.mark.asyncio
    async def test_get_detailed_order_is_called(
        self,
        use_case: GetDetailedOrderUseCase,
        order_repository: OrderRepository,
    ):
        await use_case.get_detailed_order(GetOrderDTO(order_id=1))

        order_repository.get_detailed_order.assert_awaited_once_with(1)

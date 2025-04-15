import pytest

from application.usecases.order import GetUnassignedOrderUseCase
from domain.dto.common import DetailedOrderDTO
from domain.dto.internal import LastObjectDTO
from domain.entities import DetailedOrder
from domain.repositories import OrderRepository

from .conftest import get_unassigned_order_test_data, setup_repository


class TestGetUnassignedOrderUseCase:
    @pytest.fixture
    def use_case(self, order_repository):
        return GetUnassignedOrderUseCase(order_repository)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("order, expected", get_unassigned_order_test_data)
    async def test_get_unassigned_order_success(
        self,
        use_case: GetUnassignedOrderUseCase,
        order_repository: OrderRepository,
        order: DetailedOrder,
        expected: DetailedOrderDTO,
    ):
        setup_repository(order_repository, orders=[order])

        result = await use_case.get_unassigned_order(LastObjectDTO(last_id=0))

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_unassigned_order_not_found(
        self,
        use_case: GetUnassignedOrderUseCase,
        order_repository: OrderRepository,
    ):
        setup_repository(order_repository, orders=[])

        result = await use_case.get_unassigned_order(LastObjectDTO(last_id=0))

        assert result is None

        order_repository.get_detailed_unassigned_orders_after.assert_awaited_once_with(
            0, size=1
        )

    @pytest.mark.asyncio
    async def test_get_unassigned_order_is_called(
        self,
        use_case: GetUnassignedOrderUseCase,
        order_repository: OrderRepository,
    ):
        await use_case.get_unassigned_order(LastObjectDTO(last_id=0))

        order_repository.get_detailed_unassigned_orders_after.assert_awaited_once_with(
            0, size=1
        )

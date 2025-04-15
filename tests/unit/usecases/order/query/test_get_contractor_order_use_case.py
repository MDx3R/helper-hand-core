import pytest

from application.usecases.order import (
    GetContractorDetailedOrderUseCase,
    GetContractorOrderUseCase,
    GetContractorOrderUseCaseFacade,
)
from domain.dto.common import DetailedOrderDTO, OrderDTO
from domain.dto.internal import GetUserOrderDTO
from domain.entities import DetailedOrder, Order
from domain.repositories import OrderRepository

from .conftest import (
    get_contractor_detailed_order_test_data,
    get_contractor_order_test_data,
    setup_repository,
)


class TestGetContractorOrderUseCase:
    @pytest.fixture
    def use_case(self, order_repository):
        return GetContractorOrderUseCaseFacade(order_repository)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("order, expected", get_contractor_order_test_data)
    async def test_get_contractor_order_success(
        self,
        use_case: GetContractorOrderUseCase,
        order_repository: OrderRepository,
        order: Order,
        expected: OrderDTO,
    ):
        setup_repository(order_repository, order)

        result = await use_case.get_order(
            GetUserOrderDTO(
                order_id=order.order_id, user_id=order.contractor_id or 1
            )
        )

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_contractor_order_not_found(
        self,
        use_case: GetContractorOrderUseCase,
        order_repository: OrderRepository,
    ):
        setup_repository(order_repository, None)

        result = await use_case.get_order(
            GetUserOrderDTO(order_id=999, user_id=1)
        )

        assert result is None

        order_repository.get_order_by_id_and_contractor_id.assert_awaited_once_with(
            999, 1
        )

    @pytest.mark.asyncio
    async def test_get_contractor_order_is_called(
        self,
        use_case: GetContractorOrderUseCase,
        order_repository: OrderRepository,
    ):
        await use_case.get_order(GetUserOrderDTO(order_id=1, user_id=1))

        order_repository.get_order_by_id_and_contractor_id.assert_awaited_once_with(
            1, 1
        )


class TestGetContractorDetailedOrderUseCase:
    @pytest.fixture
    def use_case(self, order_repository):
        return GetContractorOrderUseCaseFacade(order_repository)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "order, expected", get_contractor_detailed_order_test_data
    )
    async def test_get_contractor_detailed_order_success(
        self,
        use_case: GetContractorDetailedOrderUseCase,
        order_repository: OrderRepository,
        order: DetailedOrder,
        expected: DetailedOrderDTO,
    ):
        setup_repository(order_repository, order)

        result = await use_case.get_detailed_order(
            GetUserOrderDTO(
                order_id=order.order_id, user_id=order.contractor_id or 1
            )
        )

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_contractor_detailed_order_not_found(
        self,
        use_case: GetContractorDetailedOrderUseCase,
        order_repository: OrderRepository,
    ):
        setup_repository(order_repository, None)

        result = await use_case.get_detailed_order(
            GetUserOrderDTO(order_id=999, user_id=1)
        )

        assert result is None

        order_repository.get_detailed_order_by_id_and_contractor_id.assert_awaited_once_with(
            999, 1
        )

    @pytest.mark.asyncio
    async def test_get_contractor_detailed_order_is_called(
        self,
        use_case: GetContractorDetailedOrderUseCase,
        order_repository: OrderRepository,
    ):
        await use_case.get_detailed_order(
            GetUserOrderDTO(order_id=1, user_id=1)
        )

        order_repository.get_detailed_order_by_id_and_contractor_id.assert_awaited_once_with(
            1, 1
        )

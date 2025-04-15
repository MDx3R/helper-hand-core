from typing import List

import pytest

from application.usecases.order import (
    GetAdminOrdersUseCase,
    GetContracteeOrdersUseCase,
    GetContractorOrdersUseCase,
    GetUserOrdersUseCaseFacade,
)
from domain.dto.common import OrderDTO
from domain.dto.internal import GetUserOrdersDTO
from domain.entities import Order
from domain.repositories import OrderRepository

from .conftest import get_user_orders_test_data, setup_repository


class TestGetContracteeOrdersUseCase:
    @pytest.fixture
    def use_case(self, order_repository):
        return GetUserOrdersUseCaseFacade(order_repository)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("orders, expected", get_user_orders_test_data)
    async def test_get_contractee_orders_success(
        self,
        use_case: GetContracteeOrdersUseCase,
        order_repository: OrderRepository,
        orders: List[Order],
        expected: List[OrderDTO],
    ):
        setup_repository(order_repository, orders=orders)

        result = await use_case.get_contractee_orders(
            GetUserOrdersDTO(user_id=1, page=1, size=10)
        )

        assert isinstance(result, list)
        assert len(result) == len(expected)
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_contractee_orders_empty(
        self,
        use_case: GetContracteeOrdersUseCase,
        order_repository: OrderRepository,
    ):
        setup_repository(order_repository, orders=[])

        result = await use_case.get_contractee_orders(
            GetUserOrdersDTO(user_id=1, page=1, size=10)
        )

        assert result == []

    @pytest.mark.asyncio
    async def test_get_contractee_orders_is_called(
        self,
        use_case: GetContracteeOrdersUseCase,
        order_repository: OrderRepository,
    ):
        await use_case.get_contractee_orders(
            GetUserOrdersDTO(user_id=1, page=1, size=10)
        )

        order_repository.get_contractee_orders_by_page.assert_awaited_once_with(
            1, 1, 10
        )


class TestGetContractorOrdersUseCase:
    @pytest.fixture
    def use_case(self, order_repository):
        return GetUserOrdersUseCaseFacade(order_repository)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("orders, expected", get_user_orders_test_data)
    async def test_get_contractor_orders_success(
        self,
        use_case: GetContractorOrdersUseCase,
        order_repository: OrderRepository,
        orders: List[Order],
        expected: List[OrderDTO],
    ):
        setup_repository(order_repository, orders=orders)

        result = await use_case.get_contractor_orders(
            GetUserOrdersDTO(user_id=1, page=1, size=10)
        )

        assert isinstance(result, list)
        assert len(result) == len(expected)
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_contractor_orders_empty(
        self,
        use_case: GetContractorOrdersUseCase,
        order_repository: OrderRepository,
    ):
        setup_repository(order_repository, orders=[])

        result = await use_case.get_contractor_orders(
            GetUserOrdersDTO(user_id=1, page=1, size=10)
        )

        assert result == []

    @pytest.mark.asyncio
    async def test_get_contractor_orders_is_called(
        self,
        use_case: GetContractorOrdersUseCase,
        order_repository: OrderRepository,
    ):
        await use_case.get_contractor_orders(
            GetUserOrdersDTO(user_id=1, page=1, size=10)
        )

        order_repository.get_contractor_orders_by_page.assert_awaited_once_with(
            1, 1, 10
        )


class TestGetAdminOrdersUseCase:
    @pytest.fixture
    def use_case(self, order_repository):
        return GetUserOrdersUseCaseFacade(order_repository)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("orders, expected", get_user_orders_test_data)
    async def test_get_admin_orders_success(
        self,
        use_case: GetAdminOrdersUseCase,
        order_repository: OrderRepository,
        orders: List[Order],
        expected: List[OrderDTO],
    ):
        setup_repository(order_repository, orders=orders)

        result = await use_case.get_admin_orders(
            GetUserOrdersDTO(user_id=1, page=1, size=10)
        )

        assert isinstance(result, list)
        assert len(result) == len(expected)
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_admin_orders_empty(
        self,
        use_case: GetAdminOrdersUseCase,
        order_repository: OrderRepository,
    ):
        setup_repository(order_repository, orders=[])

        result = await use_case.get_admin_orders(
            GetUserOrdersDTO(user_id=1, page=1, size=10)
        )

        assert result == []

    @pytest.mark.asyncio
    async def test_get_admin_orders_is_called(
        self,
        use_case: GetAdminOrdersUseCase,
        order_repository: OrderRepository,
    ):
        await use_case.get_admin_orders(
            GetUserOrdersDTO(user_id=1, page=1, size=10)
        )

        order_repository.get_admin_orders_by_page.assert_awaited_once_with(
            1, 1, 10
        )

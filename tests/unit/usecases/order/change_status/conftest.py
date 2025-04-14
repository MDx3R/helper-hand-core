from unittest.mock import AsyncMock

import pytest

from application.usecases.order import ChangeOrderStatusUseCaseFacade
from domain.dto.context.user_context_dto import UserContextDTO
from domain.entities import Order
from domain.entities.enums import OrderStatusEnum
from tests.factories import OrderFactory, UserFactory


def setup_repository(repository: AsyncMock, order: Order):
    async def change_order_status(
        order_id: int, status: OrderStatusEnum, **kwargs
    ) -> Order:
        return Order.model_copy(order, update={"status": status, **kwargs})

    async def save_order(order: Order) -> Order:
        return order

    repository.get_order.return_value = order
    repository.change_order_status.side_effect = change_order_status
    repository.save_order.side_effect = save_order
    return repository


def setup_repository_no_order(repository: AsyncMock):
    repository.get_order.return_value = None
    return repository


def create_context():
    return UserContextDTO.model_validate(UserFactory.get_random_data())


def create_order(
    order_id=1,
    status=OrderStatusEnum.created,
    contractor_id=1,
    admin_id=None,
):
    return OrderFactory.create_model(
        order_id=order_id,
        status=status,
        contractor_id=contractor_id,
        admin_id=admin_id,
    )


@pytest.fixture
def order_repository():
    return AsyncMock()


@pytest.fixture
def use_case_facade(order_repository):
    return ChangeOrderStatusUseCaseFacade(order_repository)

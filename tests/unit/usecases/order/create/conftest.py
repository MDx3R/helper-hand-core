from typing import List
from unittest.mock import AsyncMock

import pytest

from domain.dto.context.user_context_dto import UserContextDTO
from domain.entities.order import Order
from domain.entities.order_detail import OrderDetail
from tests.factories import UserFactory

counter = 0


def set_up_counter(order_id: int):
    global counter
    counter = order_id


def create_context():
    return UserContextDTO.model_validate(UserFactory.get_random_data())


@pytest.fixture
def order_repository():
    mock = AsyncMock()

    async def save(
        order: Order,
    ) -> Order:
        data = order.get_fields()

        return order.model_validate(data | {"order_id": counter})

    mock.save.side_effect = save
    return mock


@pytest.fixture
def order_detail_repository():
    mock = AsyncMock()

    counter = 1

    async def create_details(
        details: List[OrderDetail],
    ) -> List[OrderDetail]:
        nonlocal counter
        saved_details = []
        for d in details:
            saved_details.append(
                d.model_validate(d.get_fields() | {"detail_id": counter})
            )
            counter += 1
        return saved_details

    mock.create_details.side_effect = create_details
    return mock

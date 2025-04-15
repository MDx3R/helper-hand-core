from typing import List
from unittest.mock import AsyncMock

import pytest

from domain.dto.common import DetailedOrderDTO, OrderDTO
from domain.dto.internal import (
    GetOrderDTO,
    GetUserOrderDTO,
    GetUserOrdersDTO,
    LastObjectDTO,
)
from domain.entities import Order
from tests.factories import (
    DetailedOrderFactory,
    ModelBaseFactory,
    OrderDetailFactory,
    OrderFactory,
)


def setup_repository(repository: AsyncMock, order=None, orders=None):
    repository.get_order.return_value = order
    repository.get_detailed_order.return_value = order
    repository.get_order_by_id_and_contractor_id.return_value = order
    repository.get_detailed_order_by_id_and_contractor_id.return_value = order
    repository.get_contractee_orders_by_page.return_value = orders or []
    repository.get_contractor_orders_by_page.return_value = orders or []
    repository.get_admin_orders_by_page.return_value = orders or []
    repository.get_detailed_unassigned_orders_after.return_value = orders or []
    return repository


@pytest.fixture
def order_repository():
    repository = AsyncMock()
    return setup_repository(repository, None, [])


def generate_order_test_case(
    factory: type[ModelBaseFactory], dto: type[OrderDTO]
) -> tuple[Order, OrderDTO]:
    model = factory.create_random_model()
    expected = dto.from_order(model)
    return model, expected


def generate_many_order_test_case(
    factory: type[ModelBaseFactory], dto: type[OrderDTO], count=3
) -> tuple[List[Order], List[OrderDTO]]:
    models = [factory.create_random_model() for _ in range(count)]
    expected = [dto.from_order(elem) for elem in models]
    return models, expected


# GetOrderUseCase
get_order_test_data = [
    generate_order_test_case(OrderFactory, OrderDTO),
]

get_detailed_order_test_data = [
    generate_order_test_case(DetailedOrderFactory, DetailedOrderDTO),
]

# GetContractorOrderUseCase
get_contractor_order_test_data = [
    generate_order_test_case(OrderFactory, OrderDTO),
]

get_contractor_detailed_order_test_data = [
    generate_order_test_case(DetailedOrderFactory, DetailedOrderDTO),
]

# GetUserOrdersUseCase
get_user_orders_test_data = [
    generate_many_order_test_case(OrderFactory, OrderDTO)
]

# GetUnassignedOrderUseCase
get_unassigned_order_test_data = [
    generate_order_test_case(DetailedOrderFactory, DetailedOrderDTO),
]

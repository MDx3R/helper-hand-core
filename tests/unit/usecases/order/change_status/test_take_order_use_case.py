import pytest

from application.usecases.order import TakeOrderUseCase
from domain.dto.internal import TakeOrderDTO
from domain.entities.enums import OrderStatusEnum
from domain.exceptions.service import (
    NotFoundException,
    OrderSupervisorAssignmentNotAllowedException,
)
from domain.repositories import OrderRepository

from .conftest import (
    create_context,
    create_order,
    setup_repository,
    setup_repository_no_order,
)


@pytest.fixture
def use_case(order_repository):
    return TakeOrderUseCase(order_repository)


class TestTakeOrderUseCase:
    @pytest.mark.asyncio
    async def test_take_order(
        self, use_case: TakeOrderUseCase, order_repository: OrderRepository
    ):
        context = create_context()
        order = create_order(status=OrderStatusEnum.created)
        setup_repository(order_repository, order)

        result = await use_case.take_order(
            TakeOrderDTO(order_id=order.order_id, context=context)
        )

        assert result.admin_id == context.user_id
        order_repository.save_order.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_order_not_found(
        self, use_case: TakeOrderUseCase, order_repository: OrderRepository
    ):
        context = create_context()
        setup_repository_no_order(order_repository)

        with pytest.raises(NotFoundException):
            await use_case.take_order(
                TakeOrderDTO(order_id=999, context=context)
            )

        order_repository.save_order.assert_not_awaited()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status",
        [
            OrderStatusEnum.open,
            OrderStatusEnum.active,
            OrderStatusEnum.closed,
            OrderStatusEnum.cancelled,
            OrderStatusEnum.fulfilled,
        ],
    )
    async def test_order_cannot_be_taken(
        self,
        use_case: TakeOrderUseCase,
        order_repository: OrderRepository,
        status: OrderStatusEnum,
    ):
        context = create_context()
        order = create_order(
            status=status, admin_id=1
        )  # Для всех заказов, со статусами отличными от created, должен быть куратор
        setup_repository(order_repository, order)

        with pytest.raises(OrderSupervisorAssignmentNotAllowedException):
            await use_case.take_order(
                TakeOrderDTO(order_id=order.order_id, context=context)
            )

        order_repository.save_order.assert_not_awaited()

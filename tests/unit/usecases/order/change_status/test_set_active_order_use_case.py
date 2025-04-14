import pytest

from application.usecases.order import SetActiveOrderUseCase
from domain.dto.internal import SetOrderActiveDTO
from domain.entities.enums import OrderStatusEnum
from domain.exceptions.service import (
    NotFoundException,
    OrderStatusChangeNotAllowedException,
)
from domain.exceptions.service.auth import UnauthorizedAccessException
from domain.repositories import OrderRepository

from .conftest import (
    create_context,
    create_order,
    setup_repository,
    setup_repository_no_order,
)


@pytest.fixture
def use_case(use_case_facade):
    return use_case_facade


class TestAdminSetActiveOrderUseCase:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status", [OrderStatusEnum.open, OrderStatusEnum.closed]
    )
    async def test_set_order_active(
        self,
        use_case: SetActiveOrderUseCase,
        order_repository: OrderRepository,
        status: OrderStatusEnum,
    ):
        context = create_context()
        order = create_order(status=status, admin_id=context.user_id)
        setup_repository(order_repository, order)

        result = await use_case.set_order_active(
            SetOrderActiveDTO(order_id=order.order_id, context=context)
        )

        assert result.status == OrderStatusEnum.active
        order_repository.change_order_status.assert_awaited_once_with(
            order.order_id, OrderStatusEnum.active
        )

    @pytest.mark.asyncio
    async def test_order_not_found(
        self,
        use_case: SetActiveOrderUseCase,
        order_repository: OrderRepository,
    ):
        context = create_context()
        setup_repository_no_order(order_repository)

        with pytest.raises(NotFoundException):
            await use_case.set_order_active(
                SetOrderActiveDTO(order_id=999, context=context)
            )

        order_repository.change_order_status.assert_not_awaited()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status",
        [
            OrderStatusEnum.created,
            OrderStatusEnum.active,
            OrderStatusEnum.cancelled,
            OrderStatusEnum.fulfilled,
        ],
    )
    async def test_order_cannot_be_set_active_when_status_change_not_allowed(
        self,
        use_case: SetActiveOrderUseCase,
        order_repository: OrderRepository,
        status: OrderStatusEnum,
    ):
        context = create_context()
        order = create_order(status=status, admin_id=context.user_id)
        setup_repository(order_repository, order)

        with pytest.raises(OrderStatusChangeNotAllowedException):
            await use_case.set_order_active(
                SetOrderActiveDTO(order_id=order.order_id, context=context)
            )

        order_repository.change_order_status.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_order_cannot_be_set_active_with_different_supervisor(
        self,
        use_case: SetActiveOrderUseCase,
        order_repository: OrderRepository,
    ):
        context = create_context()
        order = create_order(
            status=OrderStatusEnum.open, admin_id=context.user_id + 1
        )
        setup_repository(order_repository, order)

        with pytest.raises(UnauthorizedAccessException):
            await use_case.set_order_active(
                SetOrderActiveDTO(order_id=order.order_id, context=context)
            )

        order_repository.change_order_status.assert_not_awaited()


class TestContractorSetActiveOrderUseCase:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status", [OrderStatusEnum.open, OrderStatusEnum.closed]
    )
    async def test_set_order_active(
        self,
        use_case: SetActiveOrderUseCase,
        order_repository: OrderRepository,
        status: OrderStatusEnum,
    ):
        context = create_context()
        order = create_order(status=status, contractor_id=context.user_id)
        setup_repository(order_repository, order)

        result = await use_case.set_order_active(
            SetOrderActiveDTO(order_id=order.order_id, context=context)
        )

        assert result.status == OrderStatusEnum.active
        order_repository.change_order_status.assert_awaited_once_with(
            order.order_id, OrderStatusEnum.active
        )

    @pytest.mark.asyncio
    async def test_order_not_found(
        self,
        use_case: SetActiveOrderUseCase,
        order_repository: OrderRepository,
    ):
        context = create_context()
        setup_repository_no_order(order_repository)

        with pytest.raises(NotFoundException):
            await use_case.set_order_active(
                SetOrderActiveDTO(order_id=999, context=context)
            )

        order_repository.change_order_status.assert_not_awaited()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status",
        [
            OrderStatusEnum.created,
            OrderStatusEnum.active,
            OrderStatusEnum.cancelled,
            OrderStatusEnum.fulfilled,
        ],
    )
    async def test_order_cannot_be_set_active_when_status_change_not_allowed(
        self,
        use_case: SetActiveOrderUseCase,
        order_repository: OrderRepository,
        status: OrderStatusEnum,
    ):
        context = create_context()
        order = create_order(status=status, contractor_id=context.user_id)
        setup_repository(order_repository, order)

        with pytest.raises(OrderStatusChangeNotAllowedException):
            await use_case.set_order_active(
                SetOrderActiveDTO(order_id=order.order_id, context=context)
            )

        order_repository.change_order_status.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_order_cannot_be_set_active_with_different_contractor(
        self,
        use_case: SetActiveOrderUseCase,
        order_repository: OrderRepository,
    ):
        context = create_context()
        order = create_order(
            status=OrderStatusEnum.open, contractor_id=context.user_id + 1
        )
        setup_repository(order_repository, order)

        with pytest.raises(UnauthorizedAccessException):
            await use_case.set_order_active(
                SetOrderActiveDTO(order_id=order.order_id, context=context)
            )

        order_repository.change_order_status.assert_not_awaited()

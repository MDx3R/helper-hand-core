import pytest

from application.usecases.order import (
    ApproveOrderUseCase,
    ApproveOrderUseCaseFacade,
    DisapproveOrderUseCase,
)
from domain.dto.internal import ApproveOrderDTO
from domain.dto.internal.order import DisapproveOrderDTO
from domain.entities.enums import OrderStatusEnum
from domain.exceptions.service import NotFoundException
from domain.exceptions.service.auth import UnauthorizedAccessException
from domain.exceptions.service.orders import (
    OrderStatusChangeNotAllowedException,
)
from domain.repositories import OrderRepository

from .conftest import (
    create_context,
    create_order,
    setup_repository,
    setup_repository_no_order,
)


class TestApproveOrderUseCase:
    @pytest.fixture
    def use_case(self, order_repository):
        return ApproveOrderUseCaseFacade(order_repository)

    @pytest.mark.asyncio
    async def test_approve_order_without_admin_id(
        self,
        use_case: ApproveOrderUseCase,
        order_repository: OrderRepository,
    ):
        context = create_context()
        order = create_order(status=OrderStatusEnum.created)
        setup_repository(order_repository, order)

        result = await use_case.approve_order(
            ApproveOrderDTO(order_id=order.order_id, context=context)
        )

        assert result.status == OrderStatusEnum.open
        assert result.admin_id == context.user_id
        order_repository.save_order.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_approve_order_with_admin_id(
        self,
        use_case: ApproveOrderUseCase,
        order_repository: OrderRepository,
    ):
        context = create_context()
        order = create_order(
            status=OrderStatusEnum.created, admin_id=context.user_id
        )
        setup_repository(order_repository, order)

        result = await use_case.approve_order(
            ApproveOrderDTO(order_id=order.order_id, context=context)
        )

        assert result.status == OrderStatusEnum.open
        assert result.admin_id == context.user_id
        order_repository.save_order.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_order_not_found(
        self,
        use_case: ApproveOrderUseCase,
        order_repository: OrderRepository,
    ):
        context = create_context()
        setup_repository_no_order(order_repository)

        with pytest.raises(NotFoundException):
            await use_case.approve_order(
                ApproveOrderDTO(order_id=999, context=context)
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
    async def test_order_cannot_be_approved_when_status_change_not_allowed(
        self,
        use_case: ApproveOrderUseCase,
        order_repository: OrderRepository,
        status: OrderStatusEnum,
    ):
        context = create_context()
        order = create_order(status=status, admin_id=context.user_id)
        setup_repository(order_repository, order)

        with pytest.raises(OrderStatusChangeNotAllowedException):
            await use_case.approve_order(
                ApproveOrderDTO(order_id=order.order_id, context=context)
            )

        order_repository.save_order.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_order_cannot_be_approved_with_different_supervisor(
        self,
        use_case: ApproveOrderUseCase,
        order_repository: OrderRepository,
    ):
        context = create_context()
        order = create_order(
            status=OrderStatusEnum.created, admin_id=context.user_id + 1
        )
        setup_repository(order_repository, order)

        with pytest.raises(UnauthorizedAccessException):
            await use_case.approve_order(
                ApproveOrderDTO(order_id=order.order_id, context=context)
            )

        order_repository.save_order.assert_not_awaited()


class TestDisapproveOrderUseCase:
    @pytest.fixture
    def use_case(self, order_repository):
        return ApproveOrderUseCaseFacade(order_repository)

    @pytest.mark.asyncio
    async def test_disapprove_order_without_admin_id(
        self,
        use_case: DisapproveOrderUseCase,
        order_repository: OrderRepository,
    ):
        context = create_context()
        order = create_order(status=OrderStatusEnum.created)
        setup_repository(order_repository, order)

        result = await use_case.disapprove_order(
            DisapproveOrderDTO(order_id=order.order_id, context=context)
        )

        assert result.status == OrderStatusEnum.disapproved
        assert result.admin_id == context.user_id
        order_repository.save_order.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_approve_order_with_admin_id(
        self,
        use_case: DisapproveOrderUseCase,
        order_repository: OrderRepository,
    ):
        context = create_context()
        order = create_order(
            status=OrderStatusEnum.created, admin_id=context.user_id
        )
        setup_repository(order_repository, order)

        result = await use_case.disapprove_order(
            ApproveOrderDTO(order_id=order.order_id, context=context)
        )

        assert result.status == OrderStatusEnum.disapproved
        assert result.admin_id == context.user_id
        order_repository.save_order.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_order_not_found(
        self,
        use_case: DisapproveOrderUseCase,
        order_repository: OrderRepository,
    ):
        context = create_context()
        setup_repository_no_order(order_repository)

        with pytest.raises(NotFoundException):
            await use_case.approve_order(
                ApproveOrderDTO(order_id=999, context=context)
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
    async def test_order_cannot_be_approved_when_status_change_not_allowed(
        self,
        use_case: DisapproveOrderUseCase,
        order_repository: OrderRepository,
        status: OrderStatusEnum,
    ):
        context = create_context()
        order = create_order(status=status, admin_id=context.user_id)
        setup_repository(order_repository, order)

        with pytest.raises(OrderStatusChangeNotAllowedException):
            await use_case.disapprove_order(
                ApproveOrderDTO(order_id=order.order_id, context=context)
            )

        order_repository.save_order.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_order_cannot_be_approved_with_different_supervisor(
        self,
        use_case: DisapproveOrderUseCase,
        order_repository: OrderRepository,
    ):
        context = create_context()
        order = create_order(
            status=OrderStatusEnum.created, admin_id=context.user_id + 1
        )
        setup_repository(order_repository, order)

        with pytest.raises(UnauthorizedAccessException):
            await use_case.disapprove_order(
                ApproveOrderDTO(order_id=order.order_id, context=context)
            )

        order_repository.save_order.assert_not_awaited()

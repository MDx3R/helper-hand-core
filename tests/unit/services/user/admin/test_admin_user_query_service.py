import pytest
from tests.unit.services.user.admin.conftest import (
    AdminUserQueryServiceImpl,
    UserStatusEnum,
    setup_query_mocks,
    get_user_with_role_test_data,
    get_pending_user_test_data
)

class TestAdminUserQueryServiceImpl:
    @pytest.fixture
    def service(
        self, 
        get_user_with_role_use_case, 
        get_pending_user_use_case
    ):
        return AdminUserQueryServiceImpl(
            get_user_use_case=get_user_with_role_use_case,
            get_pending_user_use_case=get_pending_user_use_case
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user, expected", get_user_with_role_test_data)
    async def test_get_user_success(
        self,
        service: AdminUserQueryServiceImpl,
        user,
        expected
    ):
        setup_query_mocks(service, user=expected)

        result = await service.get_user(user.user_id)

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_user_not_found(
        self,
        service: AdminUserQueryServiceImpl
    ):
        setup_query_mocks(service, user=None)

        result = await service.get_user(999)

        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user, expected", get_pending_user_test_data)
    async def test_get_pending_user_success(
        self,
        service: AdminUserQueryServiceImpl,
        user,
        expected
    ):
        user.status = UserStatusEnum.pending
        expected.status = UserStatusEnum.pending
        setup_query_mocks(service, user=expected)

        result = await service.get_pending_user()

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_pending_user_not_found(
        self,
        service: AdminUserQueryServiceImpl
    ):
        setup_query_mocks(service, user=None)

        result = await service.get_pending_user()

        assert result is None

    @pytest.mark.asyncio
    async def test_get_user_calls(
        self,
        service: AdminUserQueryServiceImpl
    ):
        setup_query_mocks(service)
        await service.get_user(1)

        service.get_user_use_case.get_user_with_role.assert_awaited_once_with(1)

    @pytest.mark.asyncio
    async def test_get_pending_user_use_case_is_called(
        self,
        service: AdminUserQueryServiceImpl
    ):
        setup_query_mocks(service)
        await service.get_pending_user()

        service.get_pending_user_use_case.get_pending_user.assert_awaited_once()
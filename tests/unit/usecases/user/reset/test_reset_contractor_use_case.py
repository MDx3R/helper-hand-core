import pytest

from domain.dto.input.registration import ContractorResetDTO
from domain.dto.common import UserDTO

from application.usecases.user import (
    ResetUserUseCaseFacade,
    ResetContractorUseCase,
    ResetContractorUseCase
)

from domain.exceptions.service import InvalidInputException

from tests.generators.reset import (
    UserResetTestCaseGenerator,
    ContractorResetTestCaseGenerator,
)

def generate_test_cases():
    return [
        (t.input, t.expected) for t in [ContractorResetTestCaseGenerator.create()]
    ]

test_cases = generate_test_cases()

@pytest.fixture
def use_case(user_repository):
    service = ResetUserUseCaseFacade(
        user_repository=user_repository,
    )
    return service

@pytest.fixture
def invalid_input():
    return UserResetTestCaseGenerator.create_invalid_input().input

@pytest.fixture
def contractor_input():
    return ContractorResetTestCaseGenerator.create().input

class TestWebResetContractorUseCase:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", test_cases)
    async def test_register_contractor_is_successful(
        self, 
        use_case: ResetContractorUseCase,
        user_input: ContractorResetDTO, 
        expected_user: UserDTO
    ):
        result = await use_case.reset_contractor(user_input)
        
        assert isinstance(result, type(expected_user))
        assert result.user_id is not None
        assert isinstance(result.user_id, int)
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", test_cases)
    async def test_register_contractor_result_is_correct(
        self, 
        use_case: ResetContractorUseCase,
        user_input: ContractorResetDTO, 
        expected_user: UserDTO
    ):
        result = await use_case.reset_contractor(user_input)

        assert result == expected_user

    @pytest.mark.asyncio
    async def test_register_contractor_raises_when_invalid_input(
        self, 
        use_case: ResetUserUseCaseFacade,
        invalid_input
    ):
        with pytest.raises(InvalidInputException) as exc_info:
            await use_case.reset_contractor(invalid_input)

        use_case.user_repository.save.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_register_contractor_has_no_excessive_calls(
        self, 
        use_case: ResetUserUseCaseFacade,
        contractor_input: ContractorResetDTO
    ):
        await use_case.reset_contractor(contractor_input)

        use_case.user_repository.save.assert_awaited_once()
import pytest

from domain.dto.input.registration import ContracteeResetDTO
from domain.dto.common import UserDTO

from application.usecases.user import (
    ResetUserUseCaseFacade,
    ResetContracteeUseCase,
    ResetContracteeUseCase
)

from domain.exceptions.service import InvalidInputException

from tests.generators.reset import (
    UserResetTestCaseGenerator,
    ContracteeResetTestCaseGenerator,
)

def generate_test_cases():
    return [
        (t.input, t.expected) for t in [ContracteeResetTestCaseGenerator.create()]
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
def contractee_input():
    return ContracteeResetTestCaseGenerator.create().input

class TestWebResetContracteeUseCase:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", test_cases)
    async def test_register_contractee_is_successful(
        self, 
        use_case: ResetContracteeUseCase,
        user_input: ContracteeResetDTO, 
        expected_user: UserDTO
    ):
        result = await use_case.reset_contractee(user_input)
        
        assert isinstance(result, type(expected_user))
        assert result.user_id is not None
        assert isinstance(result.user_id, int)
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", test_cases)
    async def test_register_contractee_result_is_correct(
        self, 
        use_case: ResetContracteeUseCase,
        user_input: ContracteeResetDTO, 
        expected_user: UserDTO
    ):
        result = await use_case.reset_contractee(user_input)

        assert result == expected_user

    @pytest.mark.asyncio
    async def test_register_contractee_raises_when_invalid_input(
        self, 
        use_case: ResetUserUseCaseFacade,
        invalid_input
    ):
        with pytest.raises(InvalidInputException) as exc_info:
            await use_case.reset_contractee(invalid_input)

        use_case.user_repository.save.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_register_contractee_has_no_excessive_calls(
        self, 
        use_case: ResetUserUseCaseFacade,
        contractee_input: ContracteeResetDTO
    ):
        await use_case.reset_contractee(contractee_input)

        use_case.user_repository.save.assert_awaited_once()
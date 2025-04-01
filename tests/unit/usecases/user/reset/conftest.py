import pytest
from unittest.mock import AsyncMock

from domain.repositories import UserRepository

from tests.generators.reset import (
    UserResetTestCaseGenerator,
    ContracteeResetTestCaseGenerator,
    ContractorResetTestCaseGenerator,
)

@pytest.fixture
def invalid_input():
    return UserResetTestCaseGenerator.create_invalid_input().input

@pytest.fixture
def contractee_input():
    return ContracteeResetTestCaseGenerator.create().input

@pytest.fixture
def contractor_input():
    return ContractorResetTestCaseGenerator.create().input

def generate_contractee_test_cases():
    return [
        (t.input, t.expected) for t in [ContracteeResetTestCaseGenerator.create()]
    ]

def generate_contractor_test_cases():
    return [
        (t.input, t.expected) for t in [ContractorResetTestCaseGenerator.create()]
    ]

contractee_test_cases = generate_contractee_test_cases()
contractor_test_cases = generate_contractor_test_cases()
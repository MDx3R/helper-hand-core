import pytest
from unittest.mock import AsyncMock

from domain.dto.internal import ResetDTO

from tests.generators.reset import (
    ContracteeResetTestCaseGenerator,
    ContractorResetTestCaseGenerator,
)

@pytest.fixture
def notification_service():
    mock = AsyncMock()
    mock.send_new_registration_notification = AsyncMock(return_value=None)
    return mock

def generate_reset_contractee_test_cases():
    return [
        ContracteeResetTestCaseGenerator.create(),
    ]

def generate_reset_contractor_test_cases():
    return [
        ContractorResetTestCaseGenerator.create(),
    ]

def generate_contractee_test_cases():
    return [(t.reset, t.expected) for t in generate_reset_contractee_test_cases()]

def generate_contractor_test_cases():
    return [(t.reset, t.expected) for t in generate_reset_contractor_test_cases()]

contractee_test_cases = generate_contractee_test_cases()
contractor_test_cases = generate_contractor_test_cases()
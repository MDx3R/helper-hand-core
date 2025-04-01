import pytest
from unittest.mock import AsyncMock

from tests.generators.registration import (
    UserRegistrationTestCaseGenerator,
    ContracteeRegistrationFromTelegramTestCaseGenerator,
    ContracteeRegistrationFromWebTestCaseGenerator,
    ContractorRegistrationFromTelegramTestCaseGenerator,
    ContractorRegistrationFromWebTestCaseGenerator
)

counter = 1

@pytest.fixture
def notification_service():
    mock = AsyncMock()
    mock.send_new_registration_notification = AsyncMock(return_value=None)
    return mock

def set_up_counter(user_id: int):
    global counter
    counter = user_id

def get_counter():
    return counter

def generate_register_contractee_test_cases(generator: type[UserRegistrationTestCaseGenerator]):
    return [
        generator.create(),
    ]

def generate_register_contractor_test_cases(generator: type[UserRegistrationTestCaseGenerator]):
    return [
        generator.create(),
    ]

def generate_contractee_telegram_test_cases():
    return [(t.input, t.expected) for t in generate_register_contractee_test_cases(ContracteeRegistrationFromTelegramTestCaseGenerator)]

def generate_contractee_web_test_cases():
    return [(t.input, t.expected) for t in generate_register_contractee_test_cases(ContracteeRegistrationFromWebTestCaseGenerator)]

def generate_contractor_telegram_test_cases():
    return [(t.input, t.expected) for t in generate_register_contractor_test_cases(ContractorRegistrationFromTelegramTestCaseGenerator)]

def generate_contractor_web_test_cases():
    return [(t.input, t.expected) for t in generate_register_contractor_test_cases(ContractorRegistrationFromWebTestCaseGenerator)]

telegram_contractee_test_cases = generate_contractee_telegram_test_cases()
web_contractee_test_cases = generate_contractee_web_test_cases()
telegram_contractor_test_cases = generate_contractor_telegram_test_cases()
web_contractor_test_cases = generate_contractor_web_test_cases()
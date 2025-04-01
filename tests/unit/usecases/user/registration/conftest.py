import pytest

from tests.generators.registration import (
    UserRegistrationTestCaseGenerator,
    ContracteeRegistrationFromTelegramTestCaseGenerator,
    ContracteeRegistrationFromWebTestCaseGenerator,
    ContractorRegistrationFromTelegramTestCaseGenerator,
    ContractorRegistrationFromWebTestCaseGenerator,
)

@pytest.fixture
def invalid_input():
    return UserRegistrationTestCaseGenerator.create_invalid_input().input

@pytest.fixture
def web_contractee_input():
    return ContracteeRegistrationFromWebTestCaseGenerator.create().input

@pytest.fixture
def telegram_contractee_input():
    return ContracteeRegistrationFromTelegramTestCaseGenerator.create().input

@pytest.fixture
def web_contractor_input():
    return ContractorRegistrationFromWebTestCaseGenerator.create().input

@pytest.fixture
def telegram_contractor_input():
    return ContractorRegistrationFromTelegramTestCaseGenerator.create().input

def generate_register_user_test_cases(generator: type[UserRegistrationTestCaseGenerator]):
    return [
        generator.create(),
    ]

def generate_contractee_telegram_test_cases():
    return [(t.input, t.expected) for t in generate_register_user_test_cases(ContracteeRegistrationFromTelegramTestCaseGenerator)]

def generate_contractee_web_test_cases():
    return [(t.input, t.expected) for t in generate_register_user_test_cases(ContracteeRegistrationFromWebTestCaseGenerator)]

def generate_contractor_telegram_test_cases():
    return [(t.input, t.expected) for t in generate_register_user_test_cases(ContractorRegistrationFromTelegramTestCaseGenerator)]

def generate_contractor_web_test_cases():
    return [(t.input, t.expected) for t in generate_register_user_test_cases(ContractorRegistrationFromWebTestCaseGenerator)]

# Тестовые данные для TelegramRegisterContracteeFromWebUseCase
contractee_telegram_test_cases = generate_contractee_telegram_test_cases()

# Тестовые данные для WebRegisterContracteeFromWebUseCase
contractee_web_test_cases = generate_contractee_web_test_cases()

# Тестовые данные для TelegramRegisterContractorFromWebUseCase
contractor_telegram_test_cases = generate_contractor_telegram_test_cases()

# Тестовые данные для WebRegisterContracteeFromWebUseCase
contractor_web_test_cases = generate_contractor_web_test_cases()
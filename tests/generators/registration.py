from domain.entities.enums import UserStatusEnum

from domain.dto.input.registration import (
    UserRegistrationDTO,
    WebContracteeRegistrationDTO, TelegramContracteeRegistrationDTO,
    WebContractorRegistrationDTO, TelegramContractorRegistrationDTO
)
from domain.dto.base import ApplicationDTO
from domain.dto.context import UserContextDTO
from domain.dto.common import UserDTO, ContracteeDTO, ContractorDTO

from tests.factories import (
    AggregatedUserFactory, ContracteeFactory, ContractorFactory
)
from tests.generators.base import FactoryTestCaseGenerator

from .test_cases import UserRegistrationTestCase

class UserRegistrationTestCaseGenerator(
    FactoryTestCaseGenerator[UserRegistrationTestCase]
):
    factory: type[AggregatedUserFactory] = AggregatedUserFactory
    input_dto: type[UserRegistrationDTO] = UserRegistrationDTO
    output_dto: type[UserDTO] = UserDTO

    @classmethod
    def _create_test_case(cls, **kwargs) -> UserRegistrationTestCase:
        data = cls._get_random_data(**kwargs)

        return cls._build_test_case(data, data)

    @classmethod
    def _get_random_data(cls, **kwargs):
        return cls.factory.get_random_data(**kwargs)

    @classmethod
    def _build_test_case(cls, input, expected) -> UserRegistrationTestCase:
        return UserRegistrationTestCase(
            cls._build_input(input),
            cls._build_output(expected),
        )
    
    @classmethod
    def _build_input(cls, data) -> UserRegistrationDTO:
        return cls.input_dto.model_validate(data | {"user_id": None})
    
    @classmethod
    def _build_output(cls, data) -> UserDTO:
        return cls.output_dto.model_validate(data)

    @classmethod
    def create_invalid_input(cls) -> UserRegistrationTestCase:
        class UserInvalidInputDTO(ApplicationDTO):
            pass

        return UserRegistrationTestCase(
            UserInvalidInputDTO(),
            None
        )


class ContracteeRegistrationFromWebTestCaseGenerator(UserRegistrationTestCaseGenerator):
    factory = ContracteeFactory
    input_dto = WebContracteeRegistrationDTO
    output_dto = ContracteeDTO

    @classmethod
    def _build_input(cls, data) -> UserRegistrationDTO:
        return super()._build_input(data | {"telegram_id": None, "chat_id": None})

    @classmethod
    def _build_output(cls, data) -> ContracteeDTO:
        return super()._build_output(data | {"status": UserStatusEnum.created})


class ContracteeRegistrationFromTelegramTestCaseGenerator(UserRegistrationTestCaseGenerator):
    factory = ContracteeFactory
    input_dto = TelegramContracteeRegistrationDTO
    output_dto = ContracteeDTO

    @classmethod
    def _build_output(cls, data) -> ContracteeDTO:
        return super()._build_output(data | {"status": UserStatusEnum.pending})


class ContractorRegistrationFromWebTestCaseGenerator(UserRegistrationTestCaseGenerator):
    factory = ContractorFactory
    input_dto = WebContractorRegistrationDTO
    output_dto = ContractorDTO

    @classmethod
    def _build_input(cls, data) -> UserRegistrationDTO:
        return super()._build_input(data | {"telegram_id": None, "chat_id": None})

    @classmethod
    def _build_output(cls, data) -> ContractorDTO:
        return super()._build_output(data | {"status": UserStatusEnum.created})


class ContractorRegistrationFromTelegramTestCaseGenerator(UserRegistrationTestCaseGenerator):
    factory = ContractorFactory
    input_dto = TelegramContractorRegistrationDTO
    output_dto = ContractorDTO

    @classmethod
    def _build_output(cls, data) -> ContractorDTO:
        return super()._build_output(data | {"status": UserStatusEnum.pending})
from domain.entities.enums import UserStatusEnum

from domain.dto.input.registration import (
    UserResetDTO,
    ContracteeResetDTO, ContracteeResetDTO,
    ContractorResetDTO, ContractorResetDTO
)
from domain.dto.base import ApplicationDTO
from domain.dto.internal import ResetDTO
from domain.dto.context import UserContextDTO
from domain.dto.common import UserDTO, ContracteeDTO, ContractorDTO

from tests.factories import (
    UserFactory,
    AggregatedUserFactory, ContracteeFactory, ContractorFactory
)
from tests.generators.base import TestCaseGenerator

from .test_cases import UserResetTestCase

class UserResetTestCaseGenerator(
    TestCaseGenerator[UserResetTestCase]
):
    factory: type[AggregatedUserFactory] = AggregatedUserFactory
    input_dto: type[UserResetDTO] = UserResetDTO
    context_dto: type[UserContextDTO] = UserContextDTO
    output_dto: type[UserDTO] = UserDTO

    @classmethod
    def _create_test_case(cls, **kwargs) -> UserResetTestCase:
        data = cls._get_random_data(**kwargs)

        return cls._build_test_case(data, data, data)

    @classmethod
    def _get_random_data(cls, **kwargs):
        return cls.factory.get_random_data(**kwargs)

    @classmethod
    def _build_test_case(cls, input, context, expected) -> UserResetTestCase:
        return UserResetTestCase(
            ResetDTO(
                user=cls._build_input(input),
                context=cls._build_context(context)
            ),
            cls._build_output(expected),
        )
    
    @classmethod
    def _build_input(cls, data) -> UserResetDTO:
        return cls.input_dto.model_validate(data)
    
    @classmethod
    def _build_context(cls, data) -> UserContextDTO:
        return cls.context_dto.model_validate(data)

    @classmethod
    def _build_output(cls, data) -> UserDTO:
        return cls.output_dto.model_validate(data | {"status": UserStatusEnum.pending})

    @classmethod
    def create_invalid_input(cls) -> UserResetTestCase:
        class UserInvalidInputDTO(ApplicationDTO):
            pass

        class InputDTO(ApplicationDTO):
            user: UserInvalidInputDTO
            context: UserContextDTO

        data = UserFactory.get_random_data()

        return UserResetTestCase(
            InputDTO(
                user=UserInvalidInputDTO(),
                context=cls._build_context(data),
            ),
            None
        )
    
    @classmethod
    def create_different_id(cls) -> UserResetTestCase:
        data = cls._get_random_data()
        context = data | {"user_id": data["user_id"]+1}

        return UserResetTestCase(
            ResetDTO(
                user=cls._build_input(data),
                context=cls._build_context(context)
            ),
            None
        )


class ContracteeResetTestCaseGenerator(UserResetTestCaseGenerator):
    factory = ContracteeFactory
    input_dto = ContracteeResetDTO
    output_dto = ContracteeDTO


class ContractorResetTestCaseGenerator(UserResetTestCaseGenerator):
    factory = ContractorFactory
    input_dto = ContractorResetDTO
    output_dto = ContractorDTO
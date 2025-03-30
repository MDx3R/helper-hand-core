from domain.entities.enums import UserStatusEnum

from domain.dto.input.registration import (
    UserResetDTO,
    ContracteeResetDTO, ContracteeResetDTO,
    ContractorResetDTO, ContractorResetDTO
)
from domain.dto.base import ApplicationDTO
from domain.dto.context import UserContextDTO
from domain.dto.common import UserDTO, ContracteeDTO, ContractorDTO

from tests.creators import (
    AggregatedUserCreator, ContracteeCreator, ContractorCreator
)
from tests.generators.base import TestCaseGenerator

from .test_cases import UserResetTestCase

class UserResetTestCaseGenerator(
    TestCaseGenerator[UserResetTestCase]
):
    creator: type[AggregatedUserCreator] = AggregatedUserCreator
    input_dto: type[UserResetDTO] = UserResetDTO
    output_dto: type[UserDTO] = UserDTO

    @classmethod
    def _create_test_case(cls, **kwargs) -> UserResetTestCase:
        data = cls._get_data(random=True, **kwargs)

        return cls._build_test_case(data, data)

    @classmethod
    def _build_test_case(cls, input, expected) -> UserResetTestCase:
        return UserResetTestCase(
            cls._build_input(input),
            cls._build_output(expected),
        )
    
    @classmethod
    def _build_input(cls, data) -> UserResetDTO:
        return cls.input_dto.model_validate(data)
    
    @classmethod
    def _build_output(cls, data) -> UserDTO:
        return cls.output_dto.model_validate(data | {"status": UserStatusEnum.pending})

    @classmethod
    def _get_data(cls, random: bool = False, **kwargs):
        if random:
            return cls.creator.get_random_data(**kwargs)

        return cls.creator.get_default_data(**kwargs)

    @classmethod
    def create_invalid_input(cls) -> UserResetTestCase:
        class UserInvalidInputDTO(ApplicationDTO):
            pass

        return UserResetTestCase(
            UserInvalidInputDTO(),
            None
        )


class ContracteeResetTestCaseGenerator(UserResetTestCaseGenerator):
    creator = ContracteeCreator
    input_dto = ContracteeResetDTO
    output_dto = ContracteeDTO


class ContractorResetTestCaseGenerator(UserResetTestCaseGenerator):
    creator = ContractorCreator
    input_dto = ContractorResetDTO
    output_dto = ContractorDTO
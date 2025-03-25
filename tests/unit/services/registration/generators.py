from domain.entities.enums import UserStatusEnum

from domain.dto.input.registration import (
    UserRegistrationDTO, ContracteeRegistrationDTO, ContractorRegistrationDTO,
    TelegramContracteeRegistrationDTO, TelegramContractorRegistrationDTO,
    WebContracteeRegistrationDTO, WebContractorRegistrationDTO
)
from domain.dto.common import UserDTO, ContracteeDTO, ContractorDTO

from tests.creators import (
    AggregatedUserCreator, ContracteeCreator, ContractorCreator
)
from tests.generators.base import TestCasesGenerator

from .test_cases import UserRegistrationTestCase

class UserRegistrationTestCasesGenerator(
    TestCasesGenerator[UserRegistrationTestCase]
):
    creator: type[AggregatedUserCreator] = AggregatedUserCreator
    input_dto: type[UserRegistrationDTO] = UserRegistrationDTO
    output_dto: type[UserDTO] = UserDTO

    @classmethod
    def _create_test_case(cls, random: bool = False, **kwargs) -> UserRegistrationTestCase:
        data = cls._get_data(random, **kwargs)

        return UserRegistrationTestCase(
            cls.input_dto.model_validate(data),
            cls.output_dto.model_validate(data)
        )
    
    @classmethod
    def _get_data(cls, random: bool = False, **kwargs):
        if random:
            return cls.creator.get_random_data(**kwargs)

        return cls.creator.get_default_data(**kwargs)

    @classmethod
    def create_successful(cls, random: bool = False) -> UserRegistrationTestCase:
        return cls.create(random=random)

class TelegramUserRegistrationTestCasesGenerator(UserRegistrationTestCasesGenerator):
    @classmethod
    def _create_test_case(cls, random: bool = False, **kwargs) -> UserRegistrationTestCase:
        return super()._create_test_case(
            random=random, 
            status = UserStatusEnum.pending, 
            **kwargs
        )

class WebUserRegistrationTestCasesGenerator(UserRegistrationTestCasesGenerator):
    @classmethod
    def _create_test_case(cls, random: bool = False, **kwargs) -> UserRegistrationTestCase:
        return super()._create_test_case(
            random=random, 
            status = UserStatusEnum.created, 
            telegram_id = None,
            chat_id = None,
            **kwargs
        )

class TelegramContracteeRegistrationTestCasesGenerator(TelegramUserRegistrationTestCasesGenerator):
    creator = ContracteeCreator
    input_dto = TelegramContracteeRegistrationDTO
    output_dto = ContracteeDTO

class TelegramContractorRegistrationTestCasesGenerator(TelegramUserRegistrationTestCasesGenerator):
    creator = ContractorCreator
    input_dto = TelegramContractorRegistrationDTO
    output_dto = ContractorDTO

class WebContracteeRegistrationTestCasesGenerator(WebUserRegistrationTestCasesGenerator):
    creator = ContracteeCreator
    input_dto = WebContracteeRegistrationDTO
    output_dto = ContracteeDTO

class WebContractorRegistrationTestCasesGenerator(WebUserRegistrationTestCasesGenerator):
    creator = ContractorCreator
    input_dto = WebContractorRegistrationDTO
    output_dto = ContractorDTO
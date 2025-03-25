from domain.entities.enums import UserStatusEnum

from domain.dto.input.registration import (
    UserRegistrationDTO, UserResetDTO,
    TelegramContracteeRegistrationDTO, TelegramContractorRegistrationDTO,
    WebContracteeRegistrationDTO, WebContractorRegistrationDTO,
    ContracteeResetDTO, ContractorResetDTO
)
from domain.dto.context import UserContextDTO
from domain.dto.common import UserDTO, ContracteeDTO, ContractorDTO

from tests.creators import (
    AggregatedUserCreator, ContracteeCreator, ContractorCreator
)
from tests.generators.base import TestCasesGenerator

from .test_cases import UserRegistrationTestCase, UserResetTestCase

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
            cls.input_dto.model_validate(
                cls._concat_data(
                    data, 
                    {cls.creator.role_id_field: None, "user_id": None}
                )
            ),
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


class UserResetTestCasesGenerator(
    TestCasesGenerator[UserResetTestCase]
):
    creator: type[AggregatedUserCreator] = AggregatedUserCreator
    input_dto: type[UserResetDTO] = UserResetDTO
    output_dto: type[UserDTO] = UserDTO

    @classmethod
    def _create_test_case(cls, random: bool = False, **kwargs) -> UserResetTestCase:
        data = cls._get_data(random, **kwargs)

        return cls._build_test_case(
            input=data, 
            context=data,
            output=cls._concat_data(data, {"status": UserStatusEnum.pending})
        )

    @classmethod
    def create_successful(cls, random: bool = False) -> UserResetTestCase:
        return cls.create(random=random)
    
    @classmethod
    def create_different_telegram_id(cls, random: bool = False) -> UserResetTestCase:
        return cls.create_different_id("telegram_id", random)
    
    @classmethod
    def create_different_chat_id(cls, random: bool = False) -> UserResetTestCase:
        return cls.create_different_id("chat_id", random)

    @classmethod
    def create_different_id(cls, id_field: str = "user_id", random: bool = False) -> UserResetTestCase:
        data = cls._get_data(random)

        return cls._build_test_case(
            input=data,
            context=cls._concat_data(data, {id_field: data[id_field]+1}),
            output=data
        )

    @classmethod
    def _get_data(cls, random: bool = False, **kwargs):
        if random:
            return cls.creator.get_random_data(**kwargs)

        return cls.creator.get_default_data(**kwargs)

    @classmethod
    def _build_test_case(cls, *, input, context, output) -> UserResetTestCase:
        return UserResetTestCase(
            cls.input_dto.model_validate(input),
            UserContextDTO.model_validate(context),
            cls.output_dto.model_validate(output)
        )


class ContracteeResetTestCasesGenerator(UserResetTestCasesGenerator):
    creator = ContracteeCreator
    input_dto = ContracteeResetDTO
    output_dto = ContracteeDTO


class ContractorResetTestCasesGenerator(UserResetTestCasesGenerator):
    creator = ContractorCreator
    input_dto = ContractorResetDTO
    output_dto = ContractorDTO
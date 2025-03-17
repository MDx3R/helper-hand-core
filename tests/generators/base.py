from typing import List, TypeVar, Generic
from abc import ABC, abstractmethod

from tests.creators import ModelBaseCreator, B, M
from .test_cases import TestCase, ApplicationModelTestCase, BaseTestCase

T = TypeVar("T", bound=TestCase)

class TestCasesGenerator(ABC, Generic[T]):
    presets = {
        "default": {},
    }

    @classmethod
    def create(cls, preset_name="default", **kwargs) -> T:
        data = cls._concat_data(cls.get_preset_data(preset_name), kwargs)
        return cls._create_test_case(data)

    @classmethod
    def get_preset_data(cls, preset_name="default"):
        """Поднимает исключение, если preset_name нет в presets."""
        return cls.presets[preset_name]

    @staticmethod
    def _concat_data(d: dict, t: dict) -> dict:
        return d | t

    @classmethod
    @abstractmethod
    def _create_test_case(cls, data) -> T:
        pass

    @classmethod
    def generate_all(cls) -> List[T]:
        """Возвращает результат всех методов, начинающихся с `create_`"""
        test_cases = []
        for attr_name in dir(cls):
            if attr_name.startswith("create_"):
                method = getattr(cls, attr_name)
                if callable(method):
                    test_cases.append(method())

        return test_cases


class ApplicationModelTestCasesGenerator(TestCasesGenerator[T], Generic[T, M]):
    creator: type[ModelBaseCreator] = ModelBaseCreator
    
    @classmethod
    def _create_test_case(cls, data) -> ApplicationModelTestCase:
        return ApplicationModelTestCase(cls._create_model(data))

    @classmethod
    def _create_model(cls, data) -> M:
        return cls.creator.create_model(data)


class BaseTestCasesGenerator(TestCasesGenerator[T], Generic[T, B]):
    creator: type[ModelBaseCreator] = ModelBaseCreator
    
    @classmethod
    def _create_test_case(cls, data) -> BaseTestCase:
        return BaseTestCase(cls._create_base(data))

    @classmethod
    def _create_base(cls, data) -> B:
        return cls.creator.create_base(data)
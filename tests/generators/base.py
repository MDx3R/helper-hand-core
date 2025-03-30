from typing import Optional, List, TypeVar, Generic
from abc import ABC, abstractmethod

from tests.creators import ModelBaseCreator, B, M
from .test_cases import TestCase, ApplicationModelTestCase, BaseTestCase

T = TypeVar("T", bound=TestCase)

class TestCasesGenerator(ABC, Generic[T]):
    presets = {
        "default": {},
    }

    @classmethod
    def create(cls, preset_name: str = "default", **kwargs) -> T:
        """Создает одиночный успешный тестовый кейс."""
        data = cls._concat_data(cls.get_preset_data(preset_name), kwargs)
        return cls._create_test_case(**data)

    @classmethod
    def get_preset_data(cls, preset_name: str = "default") -> dict:
        """Получает данные из пресетов, поднимает исключение, если preset_name отсутствует."""
        if preset_name not in cls.presets:
            raise ValueError(f"'{preset_name}' не найден в {cls.__name__}.presets")
        return cls.presets[preset_name]

    @classmethod
    def create_list(cls, count: int = 3, preset_name: str = "default", **kwargs) -> List[T]:
        """Создает список тестовых случаев."""
        return [cls.create(preset_name=preset_name, **kwargs) for _ in range(count)]

    @staticmethod
    def _concat_data(d: dict, t: dict) -> dict:
        """Объединяет два словаря."""
        return d | t
    
    @classmethod
    @abstractmethod
    def _create_test_case(cls, **kwargs) -> T:
        pass


class GenerateAllTestCasesMixin:
    """Миксин для генерации всех методов create"""

    @classmethod
    def generate_all(cls, count: Optional[int] = None) -> List[T]:
        """Генерирует все тестовые случаи из методов create_*."""
        test_cases = []
        for attr_name in dir(cls):
            if attr_name.startswith("create_") and "list" not in attr_name:
                method = getattr(cls, attr_name)
                if callable(method):
                    if count is None:
                        test_cases.append(method())
                    else:
                        test_cases.extend(cls._generate_from_method(method, count))
        return test_cases
    
    @classmethod
    def _generate_from_method(cls, method, count: int) -> List[T]:
        """Вспомогательный метод для генерации списка из метода."""
        return [method() for _ in range(count)]


class ApplicationModelTestCasesGenerator(TestCasesGenerator[T], Generic[T, M]):
    creator: type[ModelBaseCreator] = ModelBaseCreator

    @classmethod
    def _create_test_case(cls, **kwargs) -> ApplicationModelTestCase:
        model = cls._create_model(random=True, **kwargs)
        return ApplicationModelTestCase(model)

    @classmethod
    def _create_model(cls, random: bool = False, **kwargs) -> M:
        if random:
            return cls.creator.create_random_model(**kwargs)
        
        return cls.creator.create_model(**kwargs)


class BaseTestCasesGenerator(TestCasesGenerator[T], Generic[T, B]):
    creator: type[ModelBaseCreator] = ModelBaseCreator

    @classmethod
    def _create_test_case(cls, **kwargs) -> BaseTestCase:
        base = cls._create_base(random=True, **kwargs)
        return BaseTestCase(base)

    @classmethod
    def _create_base(cls, random: bool = False, **kwargs) -> B:
        if random:
            return cls.creator.create_random_base(**kwargs)

        return cls.creator.create_base(**kwargs)
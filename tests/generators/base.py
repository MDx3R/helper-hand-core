from typing import Optional, List, TypeVar, Generic
from abc import ABC, abstractmethod

from tests.factories import ModelBaseFactory, B, M
from .test_cases import TestCase, ApplicationModelTestCase, BaseTestCase

T = TypeVar("T", bound=TestCase)

class TestCaseGenerator(ABC, Generic[T]):
    presets = {
        "default": {},
    }

    @classmethod
    def create(cls, preset_name: str = "default", **kwargs) -> T:
        """Создает одиночный успешный тестовый кейс."""
        data = cls.get_preset_data(preset_name) | kwargs
        return cls._create_test_case(**data)

    @classmethod
    def create_list(cls, count: int = 3, preset_name: str = "default", **kwargs) -> List[T]:
        """Создает список успешных тестовых случаев."""
        return [cls.create(preset_name=preset_name, **kwargs) for _ in range(count)]

    @classmethod
    def get_preset_data(cls, preset_name: str = "default") -> dict:
        """Получает данные из пресетов, поднимает исключение, если preset_name отсутствует."""
        if preset_name not in cls.presets:
            raise ValueError(f"'{preset_name}' не найден в {cls.__name__}.presets")
        return cls.presets[preset_name]
    
    @classmethod
    @abstractmethod
    def _create_test_case(cls, **kwargs) -> T:
        pass


class GenerateAllTestCaseMixin:
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


class FactoryTestCaseGenerator(TestCaseGenerator[T], Generic[T]):
    factory: type[ModelBaseFactory] = ModelBaseFactory


class ApplicationModelTestCaseGenerator(FactoryTestCaseGenerator[T], Generic[T, M]):
    factory: type[ModelBaseFactory] = ModelBaseFactory

    @classmethod
    def _create_test_case(cls, **kwargs) -> ApplicationModelTestCase:
        model = cls._create_model(random=True, **kwargs)
        return ApplicationModelTestCase(model)

    @classmethod
    def _create_model(cls, random: bool = False, **kwargs) -> M:
        if random:
            return cls.factory.create_random_model(**kwargs)
        
        return cls.factory.create_model(**kwargs)


class BaseTestCaseGenerator(FactoryTestCaseGenerator[T], Generic[T, B]):
    factory: type[ModelBaseFactory] = ModelBaseFactory

    @classmethod
    def _create_test_case(cls, **kwargs) -> BaseTestCase:
        base = cls._create_base(random=True, **kwargs)
        return BaseTestCase(base)

    @classmethod
    def _create_base(cls, random: bool = False, **kwargs) -> B:
        if random:
            return cls.factory.create_random_base(**kwargs)

        return cls.factory.create_base(**kwargs)
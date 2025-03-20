import pytest
from typing import List, Tuple
from domain.entities import ApplicationModel
from infrastructure.database.models import Base
from infrastructure.database.mappers import (
    ApplicationModelMapper, 
    UserMapper, 
    OrderMapper,
    OrderDetailMapper,
    ReplyMapper
)

from .test_cases import MapperTestCase
from .generators import MapperTestCasesGenerator, UserMapperTestCasesGenerator, OrderMapperTestCasesGenerator, OrderDetailMapperTestCasesGenerator, ReplyMapperTestCasesGenerator

# Список тестовых случаев
generators: list[type[MapperTestCasesGenerator]] = [
    UserMapperTestCasesGenerator,
    OrderMapperTestCasesGenerator,
    OrderDetailMapperTestCasesGenerator,
    ReplyMapperTestCasesGenerator
]

def generate_test_cases():
    test_cases = []
    for result in [generator.generate_all() for generator in generators]:
        for case in result:
            test_cases.append((case.mapper, case.base, case.model))

    return test_cases

def generate_random_test_cases():
    test_cases = []
    for result in [generator.generate_all() for generator in generators]:
        for case in result:
            test_cases.append((case.mapper, case.base, case.model))

    return test_cases

test_cases = generate_test_cases() + generate_random_test_cases()

class TestToModelApplicationModelMapper:
    @pytest.mark.parametrize("mapper, base_instance, expected_model", test_cases)
    def test_to_model_result_is_correct_instance(self, mapper: ApplicationModelMapper, base_instance: Base, expected_model: ApplicationModel) -> None:
        model = mapper.to_model(base_instance)
        assert isinstance(model, type(expected_model))

    @pytest.mark.parametrize("mapper, base_instance, expected_model", test_cases)
    def test_to_model_result_is_correct(self, mapper: ApplicationModelMapper, base_instance: Base, expected_model: ApplicationModel) -> None:
        model = mapper.to_model(base_instance)
        assert model == expected_model

    @pytest.mark.parametrize("mapper, base_instance, expected_model", test_cases)
    def test_to_model_preserves_created_at_and_updated_at(self, mapper: ApplicationModelMapper, base_instance: Base, expected_model: ApplicationModel) -> None:
        model = mapper.to_model(base_instance)
        assert model.created_at == expected_model.created_at
        assert model.updated_at == expected_model.updated_at


class TestToBaseApplicationModelMapper:
    @pytest.mark.parametrize("mapper, expected_base, model_instance", test_cases)
    def test_to_base_result_is_correct_instance(self, mapper: ApplicationModelMapper, model_instance: ApplicationModel, expected_base: Base) -> None:
        base = mapper.to_base(model_instance)
        assert isinstance(base, type(expected_base))

    @pytest.mark.parametrize("mapper, expected_base, model_instance", test_cases)
    def test_to_base_result_is_correct(self, mapper: ApplicationModelMapper, model_instance: ApplicationModel, expected_base: Base) -> None:
        base = mapper.to_base(model_instance)
        assert base.get_fields() == expected_base.get_fields()

    @pytest.mark.parametrize("mapper, expected_base, model_instance", test_cases)
    def test_to_base_preserves_created_at_and_updated_at(self, mapper: ApplicationModelMapper, model_instance: ApplicationModel, expected_base: Base) -> None:
        base = mapper.to_base(model_instance)
        assert base.created_at == expected_base.created_at
        assert base.updated_at == expected_base.updated_at

def generate_list_test_cases() -> List[Tuple[ApplicationModelMapper, List, List]]:
    """Генерирует тестовые случаи для списков, возвращая только bases и models."""
    test_cases = []
    for generator in generators:
        cases = generator.create_list(count=2, random=True)
        bases = [case.base for case in cases]
        models = [case.model for case in cases]
        test_cases.append((cases[0].mapper, bases, models))
    
    return test_cases

list_test_cases = generate_list_test_cases()

class TestToModelListApplicationModelMapper:
    @pytest.mark.parametrize("mapper, bases, expected", list_test_cases)
    def test_to_model_list_result_has_same_length(self, mapper: ApplicationModelMapper, bases: List[Base], expected: List[ApplicationModel]) -> None:
        result: List[ApplicationModel] = mapper.to_model_list(bases)
        assert len(result) == len(expected)

    @pytest.mark.parametrize("mapper, bases, expected", list_test_cases)
    def test_to_model_list_result_is_correct_instance(self, mapper: ApplicationModelMapper, bases: List[Base], expected: List[ApplicationModel]) -> None:
        result: List[ApplicationModel] = mapper.to_model_list(bases)
        for model, exp in zip(result, expected):
            assert isinstance(model, type(exp))

    @pytest.mark.parametrize("mapper, bases, expected", list_test_cases)
    def test_to_model_list_result_is_correct(self, mapper: ApplicationModelMapper, bases: List[Base], expected: List[ApplicationModel]) -> None:
        result: List[ApplicationModel] = mapper.to_model_list(bases)
        assert result == expected

    @pytest.mark.parametrize("mapper, bases, expected", list_test_cases)
    def test_to_model_list_preserves_created_at_and_updated_at(self, mapper: ApplicationModelMapper, bases: List[Base], expected: List[ApplicationModel]) -> None:
        result: List[ApplicationModel] = mapper.to_model_list(bases)
        for model, exp in zip(result, expected):
            assert model.created_at == exp.created_at
            assert model.updated_at == exp.updated_at


class TestToBaseListApplicationModelMapper:
    @pytest.mark.parametrize("mapper, expected, models", list_test_cases)
    def test_to_base_list_result_has_same_length(self, mapper: ApplicationModelMapper, expected: List[Base], models: List[ApplicationModel]) -> None:
        result: List[Base] = mapper.to_base_list(models)
        assert len(result) == len(expected)

    @pytest.mark.parametrize("mapper, expected, models", list_test_cases)
    def test_to_base_list_result_is_correct_instance(self, mapper: ApplicationModelMapper, expected: List[Base], models: List[ApplicationModel]) -> None:
        result: List[Base] = mapper.to_base_list(models)
        for base, exp in zip(result, expected):
            assert isinstance(base, type(exp))

    @pytest.mark.parametrize("mapper, expected, models", list_test_cases)
    def test_to_base_list_result_is_correct(self, mapper: ApplicationModelMapper, expected: List[Base], models: List[ApplicationModel]) -> None:
        result: List[Base] = mapper.to_base_list(models)
        for base, exp in zip(result, expected):
            assert base.get_fields() == exp.get_fields()

    @pytest.mark.parametrize("mapper, expected, models", list_test_cases)
    def test_to_base_list_preserves_created_at_and_updated_at(self, mapper: ApplicationModelMapper, expected: List[Base], models: List[ApplicationModel]) -> None:
        result: List[Base] = mapper.to_base_list(models)
        for base, exp in zip(result, expected):
            assert base.created_at == exp.created_at
            assert base.updated_at == exp.updated_at

all_mappers = [UserMapper, OrderMapper, OrderDetailMapper, ReplyMapper]

class TestApplicationModelMapperEdgeCases:
    @pytest.mark.parametrize("mapper", all_mappers)
    def test_to_model_list_with_empty_list(self, mapper: ApplicationModelMapper) -> None:
        """Проверка, что to_model_list корректно обрабатывает пустой список."""
        result: List[ApplicationModel] = mapper.to_model_list([])
        assert result == []
        assert isinstance(result, list)
        assert len(result) == 0

    @pytest.mark.parametrize("mapper", all_mappers)
    def test_to_base_list_with_empty_list(self, mapper: ApplicationModelMapper) -> None:
        """Проверка, что to_base_list корректно обрабатывает пустой список."""
        result: List[Base] = mapper.to_base_list([])
        assert result == []
        assert isinstance(result, list)
        assert len(result) == 0

    def test_to_model_with_missing_mapping(self) -> None:
        """Проверка, что to_model выбрасывает исключение при отсутствии маппинга в реестре."""
        class UnmappedBase:
            def get_fields(self):
                return {"id": 1, "name": "test"}

        unmapped_base = UnmappedBase()
        with pytest.raises(TypeError, match="Отсутствует соответствие между `UnmappedBase` и моделью"):
            ApplicationModelMapper.to_model(unmapped_base)

    def test_to_base_with_missing_mapping(self) -> None:
        """Проверка, что to_base выбрасывает исключение при отсутствии маппинга в реестре."""
        class UnmappedModel(ApplicationModel):
            def get_fields(self):
                return {"id": 1, "name": "test"}

        unmapped_model = UnmappedModel()
        with pytest.raises(TypeError, match="Отсутствует соответствие между `UnmappedModel` и моделью SQLAlchemy"):
            ApplicationModelMapper.to_base(unmapped_model)
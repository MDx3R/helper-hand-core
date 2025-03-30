import pytest
from typing import List, Tuple
from infrastructure.database.models import UserBase, Base
from infrastructure.database.mappers import AggregatedUserMapper
from domain.entities import ApplicationModel, User

from .generators import (
    AggregatedUserMapperTestCaseGenerator, 
    ContracteeMapperTestCaseGenerator, 
    ContractorMapperTestCaseGenerator, 
    AdminMapperTestCaseGenerator
)

# Список тестовых случаев
generators: list[type[AggregatedUserMapperTestCaseGenerator]] = [
    ContracteeMapperTestCaseGenerator,
    ContractorMapperTestCaseGenerator,
    AdminMapperTestCaseGenerator,
]

def generate_test_cases():
    test_cases = []
    for result in [generator.generate_all() for generator in generators]:
        for case in result:
            test_cases.append((case.mapper, case.user_base, case.role_base, case.model))
    return test_cases

test_cases = generate_test_cases()

def generate_list_test_cases() -> List[Tuple[AggregatedUserMapper, List[Tuple[UserBase, Base]], List[ApplicationModel]]]:
    """Генерирует тестовые случаи для списков, возвращая tuples из user_base и role_base, а также models."""
    test_cases = []
    for generator in generators:
        cases = generator.create_list(count=2)
        bases = [(case.user_base, case.role_base) for case in cases]
        models = [case.model for case in cases]
        test_cases.append((cases[0].mapper, bases, models))
    return test_cases

list_test_cases = generate_list_test_cases()

# Тесты для метода to_model
class TestToModelAggregatedUserMapper:
    @pytest.mark.parametrize("mapper, user_base, role_base, expected_model", test_cases)
    def test_to_model_result_is_correct_instance(self, mapper: AggregatedUserMapper, user_base: UserBase, role_base, expected_model) -> None:
        model: List[User] = mapper.to_model(user_base, role_base)
        assert isinstance(model, type(expected_model))

    @pytest.mark.parametrize("mapper, user_base, role_base, expected_model", test_cases)
    def test_to_model_result_is_correct(self, mapper: AggregatedUserMapper, user_base: UserBase, role_base, expected_model) -> None:
        model: List[User] = mapper.to_model(user_base, role_base)
        assert model == expected_model

    @pytest.mark.parametrize("mapper, user_base, role_base, expected_model", test_cases)
    def test_to_model_preserves_created_at_and_updated_at(self, mapper: AggregatedUserMapper, user_base: UserBase, role_base, expected_model) -> None:
        model: List[User] = mapper.to_model(user_base, role_base)
        assert model.created_at == expected_model.created_at
        assert model.updated_at == expected_model.updated_at

# Тесты для метода to_base
class TestToBaseAggregatedUserMapper:
    @pytest.mark.parametrize("mapper, user_base, expected_base, model_instance", test_cases)
    def test_to_base_result_is_correct_instance(self, mapper: AggregatedUserMapper, user_base: UserBase, expected_base, model_instance) -> None:
        u_base, role_base = mapper.to_base(model_instance)
        assert isinstance(role_base, type(expected_base))
        assert isinstance(u_base, UserBase)

    @pytest.mark.parametrize("mapper, user_base, expected_base, model_instance", test_cases)
    def test_to_base_result_is_correct(self, mapper: AggregatedUserMapper, user_base: UserBase, expected_base, model_instance) -> None:
        u_base, role_base = mapper.to_base(model_instance)
        assert role_base.get_fields() == expected_base.get_fields()

    @pytest.mark.parametrize("mapper, user_base, expected_base, model_instance", test_cases)
    def test_to_base_preserves_created_at_and_updated_at(self, mapper: AggregatedUserMapper, user_base: UserBase, expected_base, model_instance) -> None:
        u_base, role_base = mapper.to_base(model_instance)
        assert role_base.created_at == expected_base.created_at
        assert role_base.updated_at == expected_base.updated_at

# Тесты для метода to_model_list
class TestToModelListAggregatedUserMapper:
    @pytest.mark.parametrize("mapper, bases, expected", list_test_cases)
    def test_to_model_list_result_has_same_length(self, mapper: AggregatedUserMapper, bases: List[Tuple[UserBase, Base]], expected: List[ApplicationModel]) -> None:
        result: List[ApplicationModel] = mapper.to_model_list(bases)
        assert len(result) == len(expected)

    @pytest.mark.parametrize("mapper, bases, expected", list_test_cases)
    def test_to_model_list_result_is_correct_instance(self, mapper: AggregatedUserMapper, bases: List[Tuple[UserBase, Base]], expected: List[ApplicationModel]) -> None:
        result: List[ApplicationModel] = mapper.to_model_list(bases)
        for model, exp in zip(result, expected):
            assert isinstance(model, type(exp))

    @pytest.mark.parametrize("mapper, bases, expected", list_test_cases)
    def test_to_model_list_result_is_correct(self, mapper: AggregatedUserMapper, bases: List[Tuple[UserBase, Base]], expected: List[ApplicationModel]) -> None:
        result: List[ApplicationModel] = mapper.to_model_list(bases)
        assert result == expected

    @pytest.mark.parametrize("mapper, bases, expected", list_test_cases)
    def test_to_model_list_preserves_created_at_and_updated_at(self, mapper: AggregatedUserMapper, bases: List[Tuple[UserBase, Base]], expected: List[ApplicationModel]) -> None:
        result: List[ApplicationModel] = mapper.to_model_list(bases)
        for model, exp in zip(result, expected):
            assert model.created_at == exp.created_at
            assert model.updated_at == exp.updated_at

    @pytest.mark.parametrize("mapper", [ContracteeMapperTestCaseGenerator.mapper, ContractorMapperTestCaseGenerator.mapper, AdminMapperTestCaseGenerator.mapper])
    def test_to_model_list_with_empty_list(self, mapper: AggregatedUserMapper) -> None:
        """Проверка, что to_model_list корректно обрабатывает пустой список."""
        result: List[ApplicationModel] = mapper.to_model_list([])
        assert result == []
        assert isinstance(result, list)
        assert len(result) == 0

# Тесты для метода to_base_list
class TestToBaseListAggregatedUserMapper:
    @pytest.mark.parametrize("mapper, expected, models", list_test_cases)
    def test_to_base_list_result_has_same_length(self, mapper: AggregatedUserMapper, expected: List[Tuple[UserBase, Base]], models: List[ApplicationModel]) -> None:
        result: List[Tuple[UserBase, Base]] = mapper.to_base_list(models)
        assert len(result) == len(expected)

    @pytest.mark.parametrize("mapper, expected, models", list_test_cases)
    def test_to_base_list_result_is_correct_instance(self, mapper: AggregatedUserMapper, expected: List[Tuple[UserBase, Base]], models: List[ApplicationModel]) -> None:
        result: List[Tuple[UserBase, Base]] = mapper.to_base_list(models)
        for (user_base, role_base), (exp_user_base, exp_role_base) in zip(result, expected):
            assert isinstance(user_base, UserBase)
            assert isinstance(role_base, type(exp_role_base))

    @pytest.mark.parametrize("mapper, expected, models", list_test_cases)
    def test_to_base_list_result_is_correct(self, mapper: AggregatedUserMapper, expected: List[Tuple[UserBase, Base]], models: List[ApplicationModel]) -> None:
        result: List[Tuple[UserBase, Base]] = mapper.to_base_list(models)
        for (user_base, role_base), (exp_user_base, exp_role_base) in zip(result, expected):
            assert role_base.get_fields() == exp_role_base.get_fields()

    @pytest.mark.parametrize("mapper, expected, models", list_test_cases)
    def test_to_base_list_preserves_created_at_and_updated_at(self, mapper: AggregatedUserMapper, expected: List[Tuple[UserBase, Base]], models: List[ApplicationModel]) -> None:
        result: List[Tuple[UserBase, Base]] = mapper.to_base_list(models)
        for (user_base, role_base), (exp_user_base, exp_role_base) in zip(result, expected):
            assert role_base.created_at == exp_role_base.created_at
            assert role_base.updated_at == exp_role_base.updated_at

    @pytest.mark.parametrize("mapper", [ContracteeMapperTestCaseGenerator.mapper, ContractorMapperTestCaseGenerator.mapper, AdminMapperTestCaseGenerator.mapper])
    def test_to_base_list_with_empty_list(self, mapper: AggregatedUserMapper) -> None:
        """Проверка, что to_base_list корректно обрабатывает пустой список."""
        result: List[Tuple[UserBase, Base]] = mapper.to_base_list([])
        assert result == []
        assert isinstance(result, list)
        assert len(result) == 0
import pytest
from infrastructure.database.models import UserBase
from infrastructure.database.mappers import AggregatedUserMapper

from .generators import AggregatedUserMapperTestCasesGenerator, ContracteeMapperTestCasesGenerator, ContractorMapperTestCasesGenerator, AdminMapperTestCasesGenerator

# Список тестовых случаев
generators: list[type[AggregatedUserMapperTestCasesGenerator]] = [
    ContracteeMapperTestCasesGenerator,
    ContractorMapperTestCasesGenerator,
    AdminMapperTestCasesGenerator,
]

def generate_test_cases():
    test_cases = []
    for result in [generator.generate_all() for generator in generators]:
        for case in result:
            test_cases.append((case.mapper, case.user_base, case.role_base, case.model))

    return test_cases

test_cases = generate_test_cases()

# Тесты
class TestToModelAggregatedUserMapper:
    @pytest.mark.parametrize("mapper, user_base, role_base, expected_model", test_cases)
    def test_to_model_result_is_correct_instance(self, mapper: AggregatedUserMapper, user_base: UserBase, role_base, expected_model) -> None:
        model = mapper.to_model(user_base, role_base)
        assert isinstance(model, type(expected_model))

    @pytest.mark.parametrize("mapper, user_base, role_base, expected_model", test_cases)
    def test_to_model_result_is_correct(self, mapper: AggregatedUserMapper, user_base: UserBase, role_base, expected_model) -> None:
        model = mapper.to_model(user_base, role_base)
        assert model == expected_model

    @pytest.mark.parametrize("mapper, user_base, role_base, expected_model", test_cases)
    def test_to_model_preserves_created_at_and_updated_at(self, mapper: AggregatedUserMapper, user_base: UserBase, role_base, expected_model) -> None:
        model = mapper.to_model(user_base, role_base)
        assert model.created_at == expected_model.created_at
        assert model.updated_at == expected_model.updated_at


class TestToBaseAggregatedUserMapper:
    @pytest.mark.parametrize("mapper, user_base, expected_base, model_instance", test_cases)
    def test_to_base_result_is_correct_instance(self, mapper: AggregatedUserMapper, user_base: UserBase, expected_base, model_instance) -> None:
        user_base, role_base = mapper.to_base(model_instance)
        assert isinstance(role_base, type(expected_base))

    @pytest.mark.parametrize("mapper, user_base, expected_base, model_instance", test_cases)
    def test_to_base_result_is_correct(self, mapper: AggregatedUserMapper, user_base: UserBase, expected_base, model_instance) -> None:
        user_base, role_base = mapper.to_base(model_instance)
        assert role_base.get_fields() == expected_base.get_fields()

    @pytest.mark.parametrize("mapper, user_base, expected_base, model_instance", test_cases)
    def test_to_base_preserves_created_at_and_updated_at(self, mapper: AggregatedUserMapper, user_base: UserBase, expected_base, model_instance) -> None:
        user_base, role_base = mapper.to_base(model_instance)
        assert role_base.created_at == expected_base.created_at
        assert role_base.updated_at == expected_base.updated_at
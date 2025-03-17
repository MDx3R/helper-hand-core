import pytest
from domain.models import ApplicationModel
from infrastructure.database.models import Base
from infrastructure.database.mappers import ApplicationModelMapper

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

test_cases = generate_test_cases()

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
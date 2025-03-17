from typing import Generic, TypeVar, Tuple
import pytest
from datetime import datetime, time
from domain.models import ApplicationModel, User, Order, OrderDetail, Reply
from domain.models.enums import OrderStatusEnum, PositionEnum, GenderEnum, ReplyStatusEnum, RoleEnum, UserStatusEnum
from infrastructure.database.models import Base, UserBase, OrderBase, OrderDetailBase, ReplyBase
from infrastructure.database.mappers import BaseMapper, ApplicationModelMapper, UserMapper, OrderMapper, OrderDetailMapper, ReplyMapper

from .generators import UserTestCasesGenerator, OrderTestCasesGenerator, OrderDetailTestCasesGenerator, ReplyTestCasesGenerator

# Список тестовых случаев
test_cases = [
    UserTestCasesGenerator.create_default(),
    UserTestCasesGenerator.create_no_id(),
    UserTestCasesGenerator.create_no_patronymic(),
    UserTestCasesGenerator.create_no_photos(),
    OrderTestCasesGenerator.create_default(),
    OrderDetailTestCasesGenerator.create_default(),
    ReplyTestCasesGenerator.create_default(),
]


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
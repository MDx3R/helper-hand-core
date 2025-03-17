from typing import Generic, TypeVar, Tuple, List
from domain.models import (
    ApplicationModel,
    Contractee, Contractor, Admin
)
from infrastructure.database.models import (
    Base, 
    ContracteeBase, ContractorBase, AdminBase
)
from infrastructure.database.mappers import (
    BaseMapper, 
    ContracteeMapper, ContractorMapper, AdminMapper
)

from tests.creators import BaseCreator

M = TypeVar("M", bound=BaseMapper)
B = TypeVar("B", bound=Base)
AM = TypeVar("AM", bound=ApplicationModel)
UM = TypeVar("UM", ContracteeMapper, ContractorMapper, AdminMapper)
UB = TypeVar("UB", ContracteeBase, ContractorBase, AdminBase)
UAM = TypeVar("UAM", Contractee, Contractor, Admin)

T = TypeVar("T")

class TestCasesGenerator:
    @staticmethod
    def _concat_data(d: dict, t: dict):
        return d | t
    
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

class ApplicationModelTestCasesGenerator(TestCasesGenerator[AM], Generic[AM]):
    data = {}
    creator: type[BaseCreator] = BaseCreator
    
    @classmethod
    def _create_model(cls, data) -> AM:
        return cls.creator.create_model(data)
    
    @classmethod
    def create_default(cls, data=None, **kwargs) -> AM:
        if not data:
            data = cls.data
        data = cls._concat_data(data, kwargs)
        return cls._create_model(data)
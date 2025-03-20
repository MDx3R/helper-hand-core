from dataclasses import dataclass

from domain.entities import ApplicationModel
from infrastructure.database.models import Base

class TestCase:
    pass

@dataclass
class ApplicationModelTestCase:
    model: ApplicationModel

@dataclass
class BaseTestCase:
    base: Base
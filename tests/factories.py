from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from domain.entities.base import ApplicationModel
from domain.entities.user.admin.admin import Admin
from domain.entities.user.contractee.contractee import Contractee
from domain.entities.user.contractor.contractor import Contractor
from domain.entities.user.credentials import UserCredentials
from domain.entities.user.enums import UserStatusEnum
from domain.entities.user.user import User
from tests.builders import (
    AdminBuilder,
    ContracteeBuilder,
    ContractorBuilder,
    ModelBuilder,
    TelegramCredentialsBuilder,
    UserBuilder,
    WebCredentialsBuilder,
)
from tests.data_generators import DataGenerator

U = TypeVar("T", bound=User)
M = TypeVar("M", bound=ApplicationModel)
B = TypeVar("B", bound=ModelBuilder)
UB = TypeVar("B", bound=UserBuilder)


class BaseFactory(ABC):
    def __init__(self, generator: DataGenerator):
        self._generator = generator
        self._data = generator.generate()


class BaseUserFactory(BaseFactory, Generic[U, UB]):
    @abstractmethod
    def _builder(self) -> B:
        pass

    def create_default(self) -> U:
        return self._builder().with_status(UserStatusEnum.registered).build()

    def create_minimal(self) -> U:
        return self._builder().with_patronymic(None).with_photos([]).build()

    def create_created(self) -> U:
        return self._builder().with_status(UserStatusEnum.created).build()

    def create_pending(self) -> U:
        return self._builder().with_status(UserStatusEnum.pending).build()

    def create_disapproved(self) -> U:
        return self._builder().with_status(UserStatusEnum.disapproved).build()

    def create_dropped(self) -> U:
        return self._builder().with_status(UserStatusEnum.dropped).build()

    def create_banned(self) -> U:
        return self._builder().with_status(UserStatusEnum.banned).build()


class UserFactory(BaseUserFactory[User, UserBuilder]):
    def _builder(self):
        return UserBuilder(self._data)


class ContractorFactory(BaseUserFactory[Contractor, ContractorBuilder]):
    def _builder(self):
        return ContractorBuilder(self._data)


class ContracteeFactory(BaseUserFactory[Contractee, ContracteeBuilder]):
    def _builder(self):
        return ContracteeBuilder(self._data)


class AdminFactory(BaseUserFactory[Admin, AdminBuilder]):
    def _builder(self):
        return AdminBuilder(self._data)


class UserCredentialsFactory(BaseFactory):
    def create_default(self) -> UserCredentials:
        return UserCredentials(
            telegram=TelegramCredentialsBuilder(self._data).build(),
            web=WebCredentialsBuilder(self._data).build(),
        )

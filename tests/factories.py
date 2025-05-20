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
    BaseUserBuilder,
    ContracteeBuilder,
    ContractorBuilder,
    TelegramCredentialsBuilder,
    UserBuilder,
    WebCredentialsBuilder,
)
from tests.data_generators import DataGenerator

USER = TypeVar("USER", bound=User)
M = TypeVar("M", bound=ApplicationModel)
USER_BUILDER = TypeVar("USER_BUILDER", bound=BaseUserBuilder)


class BaseFactory(ABC):
    def __init__(self, generator: DataGenerator):
        self._generator = generator
        self._data = generator.generate()


class BaseUserFactory(BaseFactory, Generic[USER, USER_BUILDER]):
    @abstractmethod
    def _builder(self) -> USER_BUILDER:
        pass

    def create_default(self) -> USER:
        return self._builder().with_status(UserStatusEnum.registered).build()

    def create_minimal(self) -> USER:
        return self._builder().with_patronymic(None).with_photos([]).build()

    def create_created(self) -> USER:
        return self._builder().with_status(UserStatusEnum.created).build()

    def create_pending(self) -> USER:
        return self._builder().with_status(UserStatusEnum.pending).build()

    def create_disapproved(self) -> USER:
        return self._builder().with_status(UserStatusEnum.disapproved).build()

    def create_dropped(self) -> USER:
        return self._builder().with_status(UserStatusEnum.dropped).build()

    def create_banned(self) -> USER:
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

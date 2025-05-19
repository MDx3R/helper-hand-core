from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import (
    Mapping,
    Optional,
    Tuple,
    TypeVar,
    Sequence,
    List,
    Union,
    overload,
)
from sqlalchemy import Column, Select, Insert, Update, Delete
from sqlalchemy.sql.dml import (
    ReturningInsert,
    ReturningUpdate,
    ReturningDelete,
)
from sqlalchemy.engine import Result, Row
from sqlalchemy.orm.util import AliasedClass

from application.transactions.transaction_manager import TransactionManager
from infrastructure.database.models import Base

O = TypeVar("O", bound=object)

ST = Union[
    Select[Tuple[O]],
    Insert[O],
    Update[O],
    Delete[O],
]


@overload
def frozen(
    *,
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    match_args=True,
    kw_only=False,
    slots=False,
    weakref_slot=False,
):
    pass


@overload
def frozen(
    cls=None,
    /,
):
    pass


def frozen(
    cls=None,
    /,
    *,
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    match_args=True,
    kw_only=False,
    slots=False,
    weakref_slot=False,
):
    """Обертка для `dataclass`, делающая его frozen"""
    return dataclass(
        cls,
        frozen=True,
        init=init,
        repr=repr,
        eq=eq,
        order=order,
        unsafe_hash=unsafe_hash,
        match_args=match_args,
        kw_only=kw_only,
        slots=slots,
        weakref_slot=weakref_slot,
    )


class JoinType(str, Enum):
    INNER = "INNER"
    OUTER = "OUTER"


@dataclass(frozen=True)
class JoinInfo:
    left: Column
    right: Column
    join_type: Optional[JoinType] = None
    alias: Optional[str] = None


class JoinStrategy(ABC):
    def get_join(self, model: type[Base]):
        joins = self.get_strategies()
        if model not in joins:
            raise ValueError(
                f"No join strategy defined for model: {model.__name__}"
            )
        return joins[model]

    @abstractmethod
    def get_strategies(self) -> Mapping[type[Base], JoinInfo]:
        pass


@frozen(init=False)
class UnmappedEntity:
    _aliases = {}

    def __init__(self, row: Row, safe_mod: bool = True):
        annotations = self._load_all_annotations() if safe_mod else {}
        for alias, model in self._aliases.items():
            if not safe_mod or alias in annotations:
                object.__setattr__(self, alias, get_column_value(row, model))

    def _load_all_annotations(self) -> dict:
        annotations = {}
        for base in reversed(type(self).__mro__):
            annotations.update(getattr(base, "__annotations__", {}))
        return annotations


def get_column_value(
    row: Row, model: Union[type[Base], AliasedClass]
) -> Optional[Base]:
    """
    Безопасно получает атрибут из SQLAlchemy-строки Row по модели или алиасу.

    Работает как с обычными моделями, так и с aliased(model, name="...").
    """
    return row._mapping.get(model, None)


class QueryExecutor:
    def __init__(self, transaction_manager: TransactionManager):
        self.transaction_manager = transaction_manager

    async def execute_scalar_one(
        self,
        statement: (
            Select[Tuple[O]]
            | Insert[Tuple[O]]
            | Update[Tuple[O]]
            | Delete[Tuple[O]]
            | ReturningInsert[Tuple[O]]
            | ReturningUpdate[Tuple[O]]
        ),
    ) -> O | None:
        return (await self.execute(statement)).scalar_one_or_none()

    async def execute_scalar_many(
        self,
        statement: (
            Select[Tuple[O]]
            | Insert[Tuple[O]]
            | Update[Tuple[O]]
            | Delete[Tuple[O]]
            | ReturningInsert[Tuple[O]]
            | ReturningUpdate[Tuple[O]]
        ),
    ) -> List[O]:
        return (await self.execute(statement)).scalars().all()

    async def execute_one(
        self,
        statement: Select[O],
    ) -> Row[O] | None:
        return (await self.execute(statement)).one_or_none()

    async def execute_many(
        self,
        statement: Select[O],
    ) -> Sequence[Row[O]]:
        return (await self.execute(statement)).all()

    async def execute(
        self,
        statement: Select[O] | Insert[O] | Update[O] | Delete[O],
    ) -> Result[O]:
        # print(str(statement), str(statement.compile().params))
        async with self.transaction_manager.get_session() as session:
            result = await session.execute(statement)
            return result

    async def add(
        self,
        model: Base,
    ) -> None:
        async with self.transaction_manager.get_session() as session:
            session.add(model)
            await session.flush()

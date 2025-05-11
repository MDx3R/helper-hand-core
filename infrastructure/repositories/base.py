from typing import Tuple, TypeVar, Generic, Sequence, List, Union
from sqlalchemy import Select, Insert, Update, Delete, select
from sqlalchemy.engine import Result, Row
from sqlalchemy.sql import Executable

from application.transactions.transaction_manager import TransactionManager

O = TypeVar("O", bound=object)

ST = Union[
    Select[Tuple[O]],
    Insert[O],
    Update[O],
    Delete[O],
]


class QueryExecutor:
    def __init__(self, transaction_manager: TransactionManager):
        self.transaction_manager = transaction_manager

    async def execute_scalar_one(
        self,
        statement: Select[Tuple[O]],
    ) -> O | None:
        return (await self.execute(statement)).scalar_one_or_none()

    async def execute_scalar_many(
        self,
        statement: Select[Tuple[O]],
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
        async with self.transaction_manager.get_session() as session:
            result = await session.execute(statement)
            return result

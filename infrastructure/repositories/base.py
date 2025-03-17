from typing import List, TypeVar, Type, Tuple, TypeAlias
from sqlalchemy import select, exists, and_, Select, Insert, Update, Delete, Sequence
from sqlalchemy.engine import Result, Row

from application.transactions import TransactionManager

O = TypeVar("O", bound=object)

class SQLAlchemyRepository():
    def __init__(self, transaction_manager: TransactionManager):
        self.transaction_manager = transaction_manager
        
    def _calculate_offset(self, page: int, size: int) -> int:
        return (page - 1) * size if size else 0

    async def _execute_scalar_one(self, statement: Select[Tuple[O]] | Insert[Tuple[O]] | Update[Tuple[O]] | Delete[Tuple[O]]) -> O | None:
        return (await self._execute(statement)).scalar_one_or_none()
        
    async def _execute_scalar_many(self, statement: Select[Tuple[O]] | Insert[Tuple[O]] | Update[Tuple[O]] | Delete[Tuple[O]]) -> List[O]:
        return (await self._execute(statement)).scalars().all()

    async def _execute_one(self, statement: Select[Tuple[O]] | Insert[Tuple[O]] | Update[Tuple[O]] | Delete[Tuple[O]]) -> Row[O]:
        return (await self._execute(statement)).one_or_none()

    async def _execute_many(self, statement: Select[Tuple[O]] | Insert[Tuple[O]] | Update[Tuple[O]] | Delete[Tuple[O]]) -> Sequence[Row[O]]:
        return (await self._execute(statement)).all()
        
    async def _execute(self, statement: Select[Tuple[O]] | Insert[Tuple[O]] | Update[Tuple[O]] | Delete[Tuple[O]]) -> Result[O]:
        async with self.transaction_manager.get_session() as session:
            result = await session.execute(statement)
            return result
from domain.dto.reply.internal.reply_filter_dto import (
    ReplyFilterDTO,
    ContracteeReplyFilterDTO,
)
from domain.dto.base import SortingOrder
from domain.entities.reply.enums import ReplyStatusEnum
from infrastructure.repositories.reply.base import ReplyQueryBuilder
from .conftest import BaseTestQueryBuilder


class TestReplyQueryBuilder(BaseTestQueryBuilder):
    """Тесты для ReplyQueryBuilder: построение SQL-запросов."""

    def test_default_query_only_reply(self):
        builder = ReplyQueryBuilder()
        stmt = builder.build()
        sql = self._compile_sql(stmt)

        expected_starts = [f'SELECT "{self.reply_table}".reply_id']
        expected_contains = [f'FROM "{self.reply_table}"']
        unexpected = ["JOIN"]

        for part in expected_starts:
            assert sql.startswith(part)
        for part in expected_contains:
            assert part in sql
        for part in unexpected:
            assert part not in sql

    def test_join_all_entities(self):
        builder = (
            ReplyQueryBuilder().join_detail().join_order().join_contractee()
        )
        stmt = builder.build()
        sql = self._compile_sql(stmt)

        expected_joins = [
            f'JOIN "{self.order_detail_table}" ON "{self.reply_table}".detail_id = "{self.order_detail_table}".detail_id',
            f'JOIN "{self.order_table}" ON "{self.order_detail_table}".order_id = "{self.order_table}".order_id',
            f'JOIN "{self.user_table}" ON "{self.reply_table}".contractee_id = "{self.user_table}".user_id',
            f'JOIN "{self.contractee_table}" ON "{self.reply_table}".contractee_id = "{self.contractee_table}".contractee_id',
        ]

        for part in expected_joins:
            self._search(part, sql)

    def test_filter_limit_and_sorting(self):
        dto = ReplyFilterDTO(
            contractee_id=3,
            detail_id=2,
            last_id=5,
            size=50,
            sorting=SortingOrder.descending,
        )
        builder = ReplyQueryBuilder().apply_reply_filter(dto)
        stmt = builder.build()
        sql = self._compile_sql(stmt)

        expected_clauses = [
            f'"{self.reply_table}".contractee_id = {dto.contractee_id}',
            f'"{self.reply_table}".detail_id = {dto.detail_id}',
            f'"{self.reply_table}".reply_id > {dto.last_id}',
            f'ORDER BY "{self.reply_table}".created_at DESC',
            f"LIMIT {dto.size}",
        ]

        for clause in expected_clauses:
            self._search(clause, sql)

    def test_contractee_reply_filter(self):
        dto = ContracteeReplyFilterDTO(
            order_id=42,
            status=ReplyStatusEnum.accepted,
            dropped=False,
        )
        builder = ReplyQueryBuilder().apply_contractee_reply_filter(dto)
        stmt = builder.build()
        sql = self._compile_sql(stmt)

        expected_clauses = [
            f'"{self.order_detail_table}".order_id = {dto.order_id}',
            f"\"{self.reply_table}\".status = '{dto.status.value}'",
            f'"{self.reply_table}".dropped = false',
        ]
        for clause in expected_clauses:
            self._search(clause, sql)

    def test_datetime_filters(self):
        import datetime

        now = datetime.datetime(2024, 5, 1, 12, 0, 0)
        dto = ContracteeReplyFilterDTO(starts_after=now, starts_before=now)
        builder = ReplyQueryBuilder().apply_contractee_reply_filter(dto)
        stmt = builder.build()
        sql = self._compile_sql(stmt)

        self._search(rf'"{self.order_detail_table}".date\s*[><=]', sql)
        self._search(rf'"{self.order_detail_table}".start_at\s*[><=]', sql)

    def test_query_is_select_instance(self):
        builder = ReplyQueryBuilder()
        stmt = builder.build()
        from sqlalchemy.sql import Select

        assert isinstance(stmt, Select)

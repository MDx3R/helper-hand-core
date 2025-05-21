from sqlalchemy.sql import Select
from domain.dto.order.internal.order_filter_dto import OrderFilterDTO
from domain.dto.base import SortingOrder
from domain.entities.order.enums import OrderStatusEnum
from domain.entities.reply.enums import ReplyStatusEnum
from infrastructure.repositories.order.base import OrderQueryBuilder
from .conftest import BaseTestQueryBuilder


class TestOrderQueryBuilder(BaseTestQueryBuilder):
    """Тесты для OrderQueryBuilder: построение SQL-запросов."""

    def test_default_query_only_order(self):
        # Arrange
        builder = OrderQueryBuilder()

        # Act
        stmt = builder.build()
        sql = self._compile_sql(stmt)

        # Assert
        expected_starts = [f'SELECT "{self.order_table}".order_id']
        expected_contains = [f'FROM "{self.order_table}"']
        unexpected = ["JOIN"]

        for part in expected_starts:
            assert sql.startswith(part)
        for part in expected_contains:
            assert part in sql
        for part in unexpected:
            assert part not in sql

    def test_join_all_entities(self):
        # Arrange
        builder = (
            OrderQueryBuilder()
            .join_detail()
            .join_contractor()
            .join_admin()
            .join_reply()
        )

        # Act
        stmt = builder.build()
        sql = self._compile_sql(stmt)

        # Assert
        expected_joins = [
            f'JOIN "{self.order_detail_table}" ON "{self.order_table}".order_id = "{self.order_detail_table}".order_id',
            f'JOIN "{self.user_table}" AS "User_1" ON "{self.order_table}".contractor_id = "User_1".user_id',
            f'JOIN "{self.contractor_table}" ON "{self.order_table}".contractor_id = "{self.contractor_table}".contractor_id',
            f'LEFT OUTER JOIN "{self.user_table}" AS "User_2" ON "{self.order_table}".admin_id = "User_2".user_id',
            f'LEFT OUTER JOIN "{self.admin_table}" ON "{self.order_table}".admin_id = "{self.admin_table}".admin_id',
            f'LEFT OUTER JOIN "{self.reply_table}" ON "{self.order_detail_table}".detail_id = "{self.reply_table}".detail_id',
        ]

        for part in expected_joins:
            self._search(part, sql)

    def test_filter_limit_and_sorting(self):
        # Arrange
        dto = OrderFilterDTO(
            order_id=1,
            contractor_id=10,
            admin_id=5,
            status=OrderStatusEnum.active,
            size=100,
            sorting=SortingOrder.descending,
        )
        builder = OrderQueryBuilder().apply_order_filter(dto)

        # Act
        stmt = builder.build()
        sql = self._compile_sql(stmt)

        # Assert
        expected_clauses = [
            f'WHERE "{self.order_table}".order_id = {dto.order_id}',
            f"AND \"{self.order_table}\".status = '{dto.status.value}'",
            f'AND "{self.order_table}".contractor_id = {dto.contractor_id}',
            f'AND "{self.order_table}".admin_id = {dto.admin_id}',
            f'ORDER BY "{self.order_table}".created_at DESC',
            f"LIMIT {dto.size}",
        ]

        for clause in expected_clauses:
            self._search(clause, sql)

    def test_filter_by_contractee_id_joins_reply(self):
        # Arrange
        dto = OrderFilterDTO(contractee_id=7)
        builder = OrderQueryBuilder().apply_order_filter(dto)

        # Act
        stmt = builder.build()
        sql = self._compile_sql(stmt)

        # Assert
        expected_clauses = [
            f'JOIN "{self.reply_table}" ON "{self.order_detail_table}".detail_id = "{self.reply_table}".detail_id',
            f'"{self.reply_table}".contractee_id = {dto.contractee_id}',
        ]
        for clause in expected_clauses:
            self._search(clause, sql)

    def test_only_available_details_condition(self):
        # Arrange
        dto = OrderFilterDTO(only_available_details=True)
        builder = OrderQueryBuilder().apply_order_filter(dto)

        # Act
        stmt = builder.build()
        sql = self._compile_sql(stmt)

        # Assert
        regex_clauses = [
            rf'"{self.order_detail_table}".date\s*[>=<]',
            rf'"{self.order_detail_table}".start_at\s*>',
            self._normalize(
                rf"""
            SELECT count\(\*\) AS count_1 FROM "{self.reply_table}" 
            WHERE "{self.reply_table}".detail_id = "{self.order_detail_table}".detail_id 
                AND "{self.reply_table}".status = \'{ReplyStatusEnum.accepted.value}\' 
                AND "{self.reply_table}".dropped = false
            """
            ),
        ]

        for clause in regex_clauses:
            self._search(clause, sql)

    def test_query_is_select_instance(self):
        # Arrange
        builder = OrderQueryBuilder()

        # Act
        stmt = builder.build()

        # Assert
        assert isinstance(stmt, Select)

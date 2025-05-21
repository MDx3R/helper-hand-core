from sqlalchemy.sql import Select
from domain.entities.user.enums import RoleEnum, UserStatusEnum
from infrastructure.repositories.user.base import UserQueryBuilder
from domain.dto.user.internal.user_filter_dto import UserFilterDTO
from domain.dto.base import SortingOrder
from .conftest import BaseTestQueryBuilder


class TestUserQueryBuilder(BaseTestQueryBuilder):
    """Тесты для UserQueryBuilder: проверки SQL-запросов."""

    def test_default_query_no_joins(self):
        # Arrange
        builder = UserQueryBuilder()

        # Act
        stmt = builder.build()
        sql = self._compile_sql(stmt)

        # Assert
        assert sql.startswith(f'SELECT "{self.user_table}".user_id')
        assert f'FROM "{self.user_table}"' in sql
        assert "JOIN" not in sql

    def test_join_all_roles_and_credentials(self):
        # Arrange
        builder = (
            UserQueryBuilder()
            .join_admin()
            .join_contractee()
            .join_contractor()
            .join_credentials()
        )

        # Act
        stmt = builder.build()
        sql = self._compile_sql(stmt)

        # Assert
        expected_joins = [
            f'JOIN "{self.admin_table}" ON "{self.user_table}".user_id = "{self.admin_table}".admin_id',
            f'JOIN "{self.contractee_table}" ON "{self.user_table}".user_id = "{self.contractee_table}".contractee_id',
            f'JOIN "{self.contractor_table}" ON "{self.user_table}".user_id = "{self.contractor_table}".contractor_id',
            f'LEFT OUTER JOIN "{self.web_credentials_table}" ON "{self.user_table}".user_id = "{self.web_credentials_table}".user_id',
            f'LEFT OUTER JOIN "{self.telegram_credentials_table}" ON "{self.user_table}".user_id = "{self.telegram_credentials_table}".user_id',
        ]

        for part in expected_joins:
            self._search(part, sql)

    def test_filter_limit_and_sorting(self):
        # Arrange
        dto = UserFilterDTO(
            phone_number="123456",
            status=UserStatusEnum.registered,
            role=RoleEnum.admin,
            size=20,
            sorting=SortingOrder.ascending,
        )
        builder = UserQueryBuilder().apply_user_filter(dto)

        # Act
        stmt = builder.build()
        sql = self._compile_sql(stmt)

        # Assert
        expected_clauses = [
            f"WHERE \"{self.user_table}\".status = '{dto.status.value}'",
            f"AND \"{self.user_table}\".phone_number = '{dto.phone_number}'",
            f"AND \"{self.user_table}\".role = '{dto.role.value}'",
            f'ORDER BY "{self.user_table}".created_at ASC',
            f"LIMIT {dto.size}",
        ]

        for part in expected_clauses:
            self._search(part, sql)

    def test_query_is_select_instance(self):
        # Arrange
        builder = UserQueryBuilder()

        # Act
        stmt = builder.build()

        # Assert
        assert isinstance(stmt, Select)

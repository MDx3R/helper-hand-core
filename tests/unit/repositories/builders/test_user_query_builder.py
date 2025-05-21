from domain.entities.user.enums import RoleEnum, UserStatusEnum
from infrastructure.repositories.user.base import UserQueryBuilder
from domain.dto.user.internal.user_filter_dto import UserFilterDTO
from domain.dto.base import SortingOrder


class TestUserQueryBuilder:
    """Тестовый набор для класса UserQueryBuilder."""

    def _normalize(self, sql: str) -> str:
        return sql.replace("\n", " ").replace("\t", " ").strip()

    def test_default_query_no_joins(self):
        """Проверить, что по умолчанию без join'ов запрос только по таблице User."""
        stmt = UserQueryBuilder().build()
        sql = self._normalize(
            str(stmt.compile(compile_kwargs={"literal_binds": False}))
        )

        assert sql.startswith('SELECT "User".user_id')
        assert 'FROM "User"' in sql
        assert "JOIN" not in sql

    def test_join_roles_and_credentials_ordered(self):
        """Проверить, что join_{role} и join_credentials формируют корректный SQL"""
        builder = UserQueryBuilder()
        stmt = (
            builder.join_admin()
            .join_contractee()
            .join_contractor()
            .join_credentials()
            .build()
        )

        compiled_sql = str(
            stmt.compile(compile_kwargs={"literal_binds": False})
        )
        compiled_sql = self._normalize(compiled_sql)

        expected_parts = [
            'SELECT "User".user_id',
            'FROM "User"',
            'JOIN "Admin" ON "User".user_id = "Admin".admin_id',
            'JOIN "Contractee" ON "User".user_id = "Contractee".contractee_id',
            'JOIN "Contractor" ON "User".user_id = "Contractor".contractor_id',
            'LEFT OUTER JOIN "WebCredentials" ON "User".user_id = "WebCredentials".user_id',
            'LEFT OUTER JOIN "TelegramCredentials" ON "User".user_id = "TelegramCredentials".user_id',
        ]

        for part in expected_parts:
            assert part in compiled_sql, f"Missing: {part}"

    def test_filter_limit_and_sorting(self):
        """Проверить фильтр по UserFilterDTO с сортировкой и лимитом."""
        dto = UserFilterDTO(
            phone_number="123456",
            status=UserStatusEnum.registered,
            role=RoleEnum.admin,
            size=20,
            sorting=SortingOrder.ascending,
        )
        builder = UserQueryBuilder()
        stmt = builder.apply_user_filter(dto).build()
        compiled_sql = self._normalize(
            str(stmt.compile(compile_kwargs={"literal_binds": False}))
        )

        expected_parts = [
            'FROM "User"',
            'WHERE "User".status = :status_1',
            'AND "User".phone_number = :phone_number_1',
            'AND "User".role = :role_1',
            'ORDER BY "User".created_at ASC',
            "LIMIT :param_1",
        ]

        for part in expected_parts:
            assert part in compiled_sql, f"Missing: {part}"

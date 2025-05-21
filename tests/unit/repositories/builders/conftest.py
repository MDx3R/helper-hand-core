import re
from sqlalchemy.sql import Select
from infrastructure.database.models import (
    UserBase,
    AdminBase,
    ContractorBase,
    ContracteeBase,
    OrderBase,
    OrderDetailBase,
    ReplyBase,
    WebCredentialsBase,
    TelegramCredentialsBase,
)


class BaseTestQueryBuilder:
    """Базовый класс тестов для QueryBuilder"""

    user_table = UserBase.__tablename__
    admin_table = AdminBase.__tablename__
    contractee_table = ContracteeBase.__tablename__
    contractor_table = ContractorBase.__tablename__
    web_credentials_table = WebCredentialsBase.__tablename__
    telegram_credentials_table = TelegramCredentialsBase.__tablename__
    order_table = OrderBase.__tablename__
    order_detail_table = OrderDetailBase.__tablename__
    reply_table = ReplyBase.__tablename__

    def _normalize(self, sql: str) -> str:
        return re.sub(r"\s+", " ", sql.strip())

    def _compile_sql(self, stmt: Select) -> str:
        return self._normalize(
            str(stmt.compile(compile_kwargs={"literal_binds": True}))
        )

    def _search(self, part: str, sql: str):
        assert re.search(
            part, sql
        ), f"Missing (regex): {part} for (query): {sql}"

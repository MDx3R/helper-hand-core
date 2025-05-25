from decimal import Decimal
from sqlalchemy import extract, func, select, case
from application.dto.metrics.admin_metrics import AdminMetrics
from application.dto.metrics.app_metrics import AppMetrics
from application.dto.metrics.contractee_metrics import ContracteeMetrics
from application.dto.metrics.contractor_metrics import ContractorMetrics
from application.external.metrics.metrics_repository import MetricsRepository
from domain.entities.order.enums import OrderStatusEnum
from domain.entities.reply.enums import ReplyStatusEnum
from infrastructure.database.models import (
    OrderBase,
    OrderDetailBase,
    ReplyBase,
    UserBase,
)
from infrastructure.repositories.base import QueryExecutor


class MetricsRepositoryImpl(MetricsRepository):
    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    @staticmethod
    def _get_duration_hours_expr():
        """
        Возвращает выражение SQLAlchemy для продолжительности в часах между start_at и end_at,
        корректно обрабатывая ночные интервалы.
        """
        start_minutes = extract(
            "hour", OrderDetailBase.start_at
        ) * 60 + extract("minute", OrderDetailBase.start_at)
        end_minutes = extract("hour", OrderDetailBase.end_at) * 60 + extract(
            "minute", OrderDetailBase.end_at
        )
        duration_minutes = case(
            (
                end_minutes < start_minutes,
                (end_minutes + 1440) - start_minutes,
            ),
            else_=end_minutes - start_minutes,
        )
        return duration_minutes / 60.0

    async def get_app_metrics(self) -> AppMetrics:
        """Метрики по всему приложению."""
        users = select(func.count()).select_from(UserBase)
        orders = select(func.count()).select_from(OrderBase)
        replies = select(func.count()).select_from(ReplyBase)
        completed_orders = (
            select(OrderBase.order_id)
            .where(OrderBase.status == OrderStatusEnum.fulfilled)
            .subquery()
        )
        duration_hours = self._get_duration_hours_expr()
        total_amount = select(
            func.coalesce(
                func.sum(
                    OrderDetailBase.wager
                    * OrderDetailBase.count
                    * duration_hours
                ),
                0,
            )
        ).where(OrderDetailBase.order_id.in_(select(completed_orders)))
        average_wager = select(
            func.coalesce(func.avg(OrderDetailBase.wager), 0.0)
        )
        results = await self.executor.execute_one(
            select(
                users.scalar_subquery(),
                orders.scalar_subquery(),
                replies.scalar_subquery(),
                total_amount.scalar_subquery(),
                average_wager.scalar_subquery(),
            )
        )
        if not results:
            raise Exception("App metrics query returned no results")
        users, orders, replies, total_amount, average_wager = results
        return AppMetrics(
            users=users,
            orders=orders,
            replies=replies,
            total_amount=Decimal(total_amount),
            average_wager=Decimal(average_wager),
        )

    async def get_admin_metrics(self, admin_id: int) -> AdminMetrics:
        """Метрики для администратора."""
        completed_orders = (
            select(OrderBase.order_id)
            .where(
                OrderBase.admin_id == admin_id,
                OrderBase.status == OrderStatusEnum.fulfilled,
            )
            .subquery()
        )
        orders = select(func.count(OrderBase.order_id)).where(
            OrderBase.admin_id == admin_id
        )
        open_orders = select(func.count(OrderBase.order_id)).where(
            OrderBase.admin_id == admin_id,
            OrderBase.status == OrderStatusEnum.open,
        )
        active_orders = select(func.count(OrderBase.order_id)).where(
            OrderBase.admin_id == admin_id,
            OrderBase.status == OrderStatusEnum.active,
        )
        completed_orders_count = select(func.count()).select_from(
            completed_orders
        )
        duration_hours = self._get_duration_hours_expr()
        total_amount = select(
            func.coalesce(
                func.sum(
                    OrderDetailBase.wager
                    * OrderDetailBase.count
                    * duration_hours
                ),
                0,
            )
        ).where(OrderDetailBase.order_id.in_(select(completed_orders)))
        hours_worked = select(
            func.coalesce(func.sum(duration_hours * OrderDetailBase.count), 0)
        ).where(OrderDetailBase.order_id.in_(select(completed_orders)))
        results = await self.executor.execute_one(
            select(
                orders.scalar_subquery(),
                open_orders.scalar_subquery(),
                active_orders.scalar_subquery(),
                completed_orders_count.scalar_subquery(),
                total_amount.scalar_subquery(),
                hours_worked.scalar_subquery(),
            )
        )
        if not results:
            raise Exception("Admin metrics query returned no results")
        (
            orders,
            open_orders,
            active_orders,
            completed_orders_count,
            total_amount,
            hours_worked,
        ) = results
        return AdminMetrics(
            orders=orders,
            open_orders=open_orders,
            active_orders=active_orders,
            completed_orders=completed_orders_count,
            amount=Decimal(total_amount),
            hours_worked=hours_worked,
        )

    async def get_contractee_metrics(
        self, contractee_id: int
    ) -> ContracteeMetrics:
        """Метрики для исполнителя (contractee)."""
        duration_hours = self._get_duration_hours_expr()
        completed_orders = (
            select(OrderBase.order_id)
            .where(OrderBase.status == OrderStatusEnum.fulfilled)
            .scalar_subquery()
        )
        replies = select(func.count(ReplyBase.reply_id)).where(
            ReplyBase.contractee_id == contractee_id
        )
        accepted_replies = select(func.count(ReplyBase.reply_id)).where(
            ReplyBase.contractee_id == contractee_id,
            ReplyBase.status == ReplyStatusEnum.accepted,
            ReplyBase.dropped == False,
        )
        accepted_details = (
            select(ReplyBase.detail_id)
            .where(
                ReplyBase.contractee_id == contractee_id,
                ReplyBase.status == ReplyStatusEnum.accepted,
                ReplyBase.dropped == False,
            )
            .subquery()
        )
        orders_with_accepted_replies = select(
            func.count(func.distinct(OrderDetailBase.order_id))
        ).where(OrderDetailBase.detail_id.in_(select(accepted_details)))
        earned = select(
            func.coalesce(
                func.sum(
                    OrderDetailBase.wager
                    * OrderDetailBase.count
                    * duration_hours
                ),
                0,
            )
        ).where(OrderDetailBase.order_id.in_(select(completed_orders)))
        hours_worked = select(
            func.coalesce(func.sum(duration_hours * OrderDetailBase.count), 0)
        ).where(OrderDetailBase.order_id.in_(select(completed_orders)))
        average_wager = select(
            func.coalesce(func.avg(OrderDetailBase.wager), 0.0)
        ).where(OrderDetailBase.order_id.in_(select(completed_orders)))
        results = await self.executor.execute_one(
            select(
                replies.scalar_subquery(),
                accepted_replies.scalar_subquery(),
                orders_with_accepted_replies.scalar_subquery(),
                earned.scalar_subquery(),
                hours_worked.scalar_subquery(),
                average_wager.scalar_subquery(),
            )
        )
        if not results:
            raise Exception("Contractee metrics query returned no results")
        (
            replies,
            accepted_replies,
            orders_with_accepted_replies,
            earned,
            hours_worked,
            average_wager,
        ) = results
        return ContracteeMetrics(
            replies=replies,
            accepted_replies=accepted_replies,
            orders_with_accepted_replies=orders_with_accepted_replies,
            earned=Decimal(earned),
            hours_worked=hours_worked,
            average_wager=Decimal(average_wager),
        )

    async def get_contractor_metrics(
        self, contractor_id: int
    ) -> ContractorMetrics:
        """Метрики для заказчика (contractor)."""
        duration_hours = self._get_duration_hours_expr()
        completed_orders = (
            select(OrderBase.order_id)
            .where(
                OrderBase.contractor_id == contractor_id,
                OrderBase.status == OrderStatusEnum.fulfilled,
            )
            .subquery()
        )
        orders = select(func.count(OrderBase.order_id)).where(
            OrderBase.contractor_id == contractor_id
        )
        open_orders = select(func.count(OrderBase.order_id)).where(
            OrderBase.contractor_id == contractor_id,
            OrderBase.status == OrderStatusEnum.open,
        )
        active_orders = select(func.count(OrderBase.order_id)).where(
            OrderBase.contractor_id == contractor_id,
            OrderBase.status == OrderStatusEnum.active,
        )
        completed_orders_count = select(func.count()).select_from(
            completed_orders
        )
        replies = (
            select(func.count(ReplyBase.reply_id))
            .join(
                OrderDetailBase,
                ReplyBase.detail_id == OrderDetailBase.detail_id,
            )
            .join(OrderBase, OrderDetailBase.order_id == OrderBase.order_id)
            .where(OrderBase.contractor_id == contractor_id)
        )
        pending_replies = (
            select(func.count(ReplyBase.reply_id))
            .join(
                OrderDetailBase,
                ReplyBase.detail_id == OrderDetailBase.detail_id,
            )
            .join(OrderBase, OrderDetailBase.order_id == OrderBase.order_id)
            .where(
                OrderBase.contractor_id == contractor_id,
                ReplyBase.status == ReplyStatusEnum.created,
                ReplyBase.dropped == False,
            )
        )
        total_amount = select(
            func.coalesce(
                func.sum(
                    OrderDetailBase.wager
                    * OrderDetailBase.count
                    * duration_hours
                ),
                0,
            )
        ).where(OrderDetailBase.order_id.in_(select(completed_orders)))
        hours_worked = select(
            func.coalesce(func.sum(duration_hours * OrderDetailBase.count), 0)
        ).where(OrderDetailBase.order_id.in_(select(completed_orders)))
        results = await self.executor.execute_one(
            select(
                orders.scalar_subquery(),
                open_orders.scalar_subquery(),
                active_orders.scalar_subquery(),
                completed_orders_count.scalar_subquery(),
                replies.scalar_subquery(),
                pending_replies.scalar_subquery(),
                total_amount.scalar_subquery(),
                hours_worked.scalar_subquery(),
            )
        )
        if not results:
            raise Exception("Contractor metrics query returned no results")
        (
            orders,
            open_orders,
            active_orders,
            completed_orders_count,
            replies,
            pending_replies,
            spent,
            hours_worked,
        ) = results
        return ContractorMetrics(
            orders=orders,
            open_orders=open_orders,
            active_orders=active_orders,
            completed_orders=completed_orders_count,
            replies=replies,
            pending_replies=pending_replies,
            spent=Decimal(spent),
            hours_worked=hours_worked,
        )

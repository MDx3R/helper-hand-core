from application.dto.metrics.admin_metrics import AdminMetrics
from application.external.metrics.metrics_repository import MetricsRepository
from domain.dto.user.internal.user_context_dto import UserContextDTO


class GetAdminMetricsUseCase:
    def __init__(self, service: MetricsRepository) -> None:
        self.service = service

    async def execute(self, context: UserContextDTO) -> AdminMetrics:
        return await self.service.get_admin_metrics(context.user_id)

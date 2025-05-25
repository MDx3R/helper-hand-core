from application.dto.metrics.admin_metrics import AdminMetrics
from application.external.metrics.metrics_repository import MetricsRepository


class GetAdminMetricsUseCase:
    def __init__(self, service: MetricsRepository) -> None:
        self.service = service

    async def execute(self, admin_id: int) -> AdminMetrics:
        return await self.service.get_admin_metrics(admin_id)

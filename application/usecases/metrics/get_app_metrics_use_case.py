from application.dto.metrics.app_metrics import AppMetrics
from application.external.metrics.metrics_repository import MetricsRepository


class GetAppMetricsUseCase:
    def __init__(self, service: MetricsRepository) -> None:
        self.service = service

    async def execute(self) -> AppMetrics:
        return await self.service.get_app_metrics()

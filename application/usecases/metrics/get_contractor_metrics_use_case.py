from application.dto.metrics.contractor_metrics import ContractorMetrics
from application.external.metrics.metrics_repository import MetricsRepository


class GetContractorMetricsUseCase:
    def __init__(self, service: MetricsRepository) -> None:
        self.service = service

    async def execute(self, contractor_id: int) -> ContractorMetrics:
        return await self.service.get_contractor_metrics(contractor_id)

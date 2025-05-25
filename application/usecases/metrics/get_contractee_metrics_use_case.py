from application.dto.metrics.contractee_metrics import ContracteeMetrics
from application.external.metrics.metrics_service import MetricsRepository


class GetContracteeMetricsUseCase:
    def __init__(self, service: MetricsRepository) -> None:
        self.service = service

    async def execute(self, contractee_id: int) -> ContracteeMetrics:
        return await self.service.get_contractee_metrics(contractee_id)

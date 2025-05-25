from application.dto.metrics.contractor_metrics import ContractorMetrics
from application.external.metrics.metrics_repository import MetricsRepository
from domain.dto.user.internal.user_context_dto import UserContextDTO


class GetContractorMetricsUseCase:
    def __init__(self, service: MetricsRepository) -> None:
        self.service = service

    async def execute(self, context: UserContextDTO) -> ContractorMetrics:
        return await self.service.get_contractor_metrics(context.user_id)

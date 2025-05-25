from application.dto.metrics.contractee_metrics import ContracteeMetrics
from application.external.metrics.metrics_repository import MetricsRepository
from domain.dto.user.internal.user_context_dto import UserContextDTO


class GetContracteeMetricsUseCase:
    def __init__(self, service: MetricsRepository) -> None:
        self.service = service

    async def execute(self, context: UserContextDTO) -> ContracteeMetrics:
        return await self.service.get_contractee_metrics(context.user_id)

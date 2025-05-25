from application.dto.metrics.admin_metrics import AdminMetrics
from application.dto.metrics.app_metrics import AppMetrics
from application.dto.metrics.contractee_metrics import ContracteeMetrics
from application.dto.metrics.contractor_metrics import ContractorMetrics
from application.external.metrics.metrics_service import MetricsService
from application.usecases.metrics.get_admin_metrics_use_case import (
    GetAdminMetricsUseCase,
)
from application.usecases.metrics.get_app_metrics_use_case import (
    GetAppMetricsUseCase,
)
from application.usecases.metrics.get_contractee_metrics_use_case import (
    GetContracteeMetricsUseCase,
)
from application.usecases.metrics.get_contractor_metrics_use_case import (
    GetContractorMetricsUseCase,
)
from domain.dto.user.internal.user_context_dto import UserContextDTO


class MetricsServiceImpl(MetricsService):
    def __init__(
        self,
        get_app_metrics_use_case: GetAppMetricsUseCase,
        get_admin_metrics_use_case: GetAdminMetricsUseCase,
        get_contractee_metrics_use_case: GetContracteeMetricsUseCase,
        get_contractor_metrics_use_case: GetContractorMetricsUseCase,
    ) -> None:
        self.get_app_metrics_use_case = get_app_metrics_use_case
        self.get_admin_metrics_use_case = get_admin_metrics_use_case
        self.get_contractee_metrics_use_case = get_contractee_metrics_use_case
        self.get_contractor_metrics_use_case = get_contractor_metrics_use_case

    async def get_app_metrics(self) -> AppMetrics:
        return await self.get_app_metrics_use_case.execute()

    async def get_admin_metrics(self, context: UserContextDTO) -> AdminMetrics:
        return await self.get_admin_metrics_use_case.execute(context)

    async def get_contractee_metrics(
        self, context: UserContextDTO
    ) -> ContracteeMetrics:
        return await self.get_contractee_metrics_use_case.execute(context)

    async def get_contractor_metrics(
        self, context: UserContextDTO
    ) -> ContractorMetrics:
        return await self.get_contractor_metrics_use_case.execute(context)

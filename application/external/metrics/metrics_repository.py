from abc import ABC, abstractmethod

from application.dto.metrics.admin_metrics import AdminMetrics
from application.dto.metrics.app_metrics import AppMetrics
from application.dto.metrics.contractee_metrics import ContracteeMetrics
from application.dto.metrics.contractor_metrics import ContractorMetrics


class MetricsRepository(ABC):
    @abstractmethod
    async def get_app_metrics(self) -> AppMetrics: ...
    @abstractmethod
    async def get_admin_metrics(self, admin_id: int) -> AdminMetrics: ...
    @abstractmethod
    async def get_contractee_metrics(
        self, contractee_id: int
    ) -> ContracteeMetrics: ...
    @abstractmethod
    async def get_contractor_metrics(
        self, contractor_id: int
    ) -> ContractorMetrics: ...

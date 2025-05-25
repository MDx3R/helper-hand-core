from abc import ABC, abstractmethod

from application.dto.metrics.admin_metrics import AdminMetrics
from application.dto.metrics.app_metrics import AppMetrics
from application.dto.metrics.contractee_metrics import ContracteeMetrics
from application.dto.metrics.contractor_metrics import ContractorMetrics
from domain.dto.user.internal.user_context_dto import UserContextDTO


class MetricsService(ABC):
    @abstractmethod
    async def get_app_metrics(self) -> AppMetrics: ...
    @abstractmethod
    async def get_admin_metrics(
        self, context: UserContextDTO
    ) -> AdminMetrics: ...
    @abstractmethod
    async def get_contractee_metrics(
        self, context: UserContextDTO
    ) -> ContracteeMetrics: ...
    @abstractmethod
    async def get_contractor_metrics(
        self, context: UserContextDTO
    ) -> ContractorMetrics: ...

from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from core.containers import Container
from application.services.metrics.metrics_service import MetricsServiceImpl
from domain.dto.user.internal.user_context_dto import UserContextDTO
from application.dto.metrics.app_metrics import AppMetrics
from application.dto.metrics.admin_metrics import AdminMetrics
from application.dto.metrics.contractee_metrics import ContracteeMetrics
from application.dto.metrics.contractor_metrics import ContractorMetrics
from presentation.controllers.permissions import (
    is_admin,
    is_contractee,
    is_contractor,
    require_admin,
    require_contractee,
    require_contractor,
)
from fastapi_utils.cbv import cbv

app_router = APIRouter()
admin_router = APIRouter(dependencies=[Depends(is_admin)])
contractee_router = APIRouter(dependencies=[Depends(is_contractee)])
contractor_router = APIRouter(dependencies=[Depends(is_contractor)])


@inject
def get_metrics_service(
    service: MetricsServiceImpl = Depends(Provide[Container.metrics_service]),
) -> MetricsServiceImpl:
    return service


@cbv(app_router)
class AppMetricsController:
    service: MetricsServiceImpl = Depends(get_metrics_service)

    @app_router.get("/", response_model=AppMetrics)
    async def get_app_metrics(self):
        return await self.service.get_app_metrics()


@cbv(admin_router)
class AdminMetricsController:
    service: MetricsServiceImpl = Depends(get_metrics_service)

    @admin_router.get("/", response_model=AdminMetrics)
    async def get_admin_metrics(
        self, user: UserContextDTO = Depends(require_admin)
    ):
        return await self.service.get_admin_metrics(user)


@cbv(contractee_router)
class ContracteeMetricsController:
    service: MetricsServiceImpl = Depends(get_metrics_service)

    @contractee_router.get("/", response_model=ContracteeMetrics)
    async def get_contractee_metrics(
        self, user: UserContextDTO = Depends(require_contractee)
    ):
        return await self.service.get_contractee_metrics(user)


@cbv(contractor_router)
class ContractorMetricsController:
    service: MetricsServiceImpl = Depends(get_metrics_service)

    @contractor_router.get("/", response_model=ContractorMetrics)
    async def get_contractor_metrics(
        self, user: UserContextDTO = Depends(require_contractor)
    ):
        return await self.service.get_contractor_metrics(user)

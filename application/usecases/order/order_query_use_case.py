from abc import ABC, abstractmethod
from typing import List

from domain.dto.common import DetailedOrderDTO, OrderDTO, OrderDetailDTO

# Базовые Use Case для запросов
class GetOrderUseCase(ABC):
    @abstractmethod
    async def get_order(self, order_id: int) -> OrderDTO | None:
        pass

class GetDetailedOrderUseCase(ABC):
    @abstractmethod
    async def get_detailed_order(self, order_id: int) -> DetailedOrderDTO | None:
        pass

class GetContracteeOrdersUseCase(ABC):
    @abstractmethod
    async def get_contractee_orders(self, contractee_id: int, page: int = 1, size: int = 15) -> List[OrderDTO]:
        pass

class GetContractorOrdersUseCase(ABC):
    @abstractmethod
    async def get_contractor_orders(self, contractor_id: int, page: int = 1, size: int = 15) -> List[OrderDTO]:
        pass

class GetAdminOrdersUseCase(ABC):
    @abstractmethod
    async def get_contractor_orders(self, contractor_id: int, page: int = 1, size: int = 15) -> List[OrderDTO]:
        pass

# Специфичные Use Case
class GetUnassignedOrderUseCase(ABC):
    @abstractmethod
    async def get_unassigned_order(self, last_order_id: int = None) -> DetailedOrderDTO | None:
        pass

class GetOpenOrderUseCase(ABC):
    @abstractmethod
    async def get_open_order(self, last_order_id: int = None) -> DetailedOrderDTO | None:
        pass

class GetAvailableDetailsUseCase(ABC):
    @abstractmethod
    async def get_available_details(self, order_id: int, contractee_id: int) -> List[OrderDetailDTO]:
        pass

# Фасад для всех запросов и фильтров
class OrderQueryUseCaseFacade(
    GetOrderUseCase,
    GetDetailedOrderUseCase,
    GetContracteeOrdersUseCase,
    GetContractorOrdersUseCase,
    GetAvailableDetailsUseCase,
    GetAdminOrdersUseCase,
):
    pass
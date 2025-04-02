from abc import ABC, abstractmethod
from typing import List

from domain.dto.common import OrderDTO, DetailedOrderDTO
from domain.dto.internal import GetUserOrdersDTO, PaginationDTO

class ContracteeAssociatedOrderQueryService(ABC):
    """Интерфейс сервисов для запроса заказов исполнителей"""
    @abstractmethod
    async def get_orders(self, query: GetUserOrdersDTO) -> List[OrderDTO]:
        pass

    # TODO: Добавить методы получения заказов по статусам

class ContractorAssociatedOrderQueryService(ABC):
    """Интерфейс сервисов для запроса заказов заказчиков"""
    @abstractmethod
    async def get_orders(self, query: GetUserOrdersDTO) -> List[OrderDTO]:
        pass

    # TODO: Добавить методы получения заказов по статусам

class AdminAssociatedOrderQueryService(ABC):
    """Интерфейс сервисов для запроса заказов администраторов"""
    @abstractmethod
    async def get_orders(self, query: GetUserOrdersDTO) -> List[OrderDTO]:
        pass

    @abstractmethod
    async def get_open_orders(self, query: GetUserOrdersDTO) -> List[OrderDTO]:
        pass

    @abstractmethod
    async def get_closed_orders(self, query: GetUserOrdersDTO) -> List[OrderDTO]:
        pass

    @abstractmethod
    async def get_active_orders(self, query: GetUserOrdersDTO) -> List[OrderDTO]:
        pass

    # TODO: Дополнить методы получения заказов по статусам

class OrderStatusFilterService(ABC):
    @abstractmethod
    # TODO: Установить тип query как запрос с контекстом: status, contactor_id и т.п.
    # NOTE: Можно перенести/переопределить похожие методы из {User}AssociatedOrderQueryService
    async def get_open_orders(self, query: PaginationDTO) -> List[OrderDTO]:
        pass

    @abstractmethod
    async def get_closed_orders(self, query: PaginationDTO) -> List[OrderDTO]:
        pass

    @abstractmethod
    async def get_active_orders(self, query: PaginationDTO) -> List[OrderDTO]:
        pass
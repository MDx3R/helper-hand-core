from abc import ABC, abstractmethod
from domain.dto.common import OrderDTO
from domain.dto.context import UserContextDTO

class CancelOrderUseCase(ABC):
    @abstractmethod
    async def cancel_order(self, order_id: int) -> OrderDTO:
        pass

class SetActiveOrderUseCase(ABC):
    @abstractmethod
    async def set_order_active(self, order_id: int) -> OrderDTO:
        pass

class TakeOrderUseCase(ABC):
    @abstractmethod
    async def take_order(self, order_id: int, context: UserContextDTO) -> OrderDTO:
        pass

class ApproveOrderUseCase(ABC):
    @abstractmethod
    async def approve_order(self, order_id: int) -> OrderDTO:
        pass

class CancelOrderUseCase(ABC):
    @abstractmethod
    async def cancel_order(self, order_id: int) -> OrderDTO:
        pass

class CloseOrderUseCase(ABC):
    @abstractmethod
    async def close_order(self, order_id: int) -> OrderDTO:
        pass

class OpenOrderUseCase(ABC):
    @abstractmethod
    async def open_order(self, order_id: int) -> OrderDTO:
        pass

class FulfillOrderUseCase(ABC):
    @abstractmethod
    async def fulfill_order(self, order_id: int) -> OrderDTO:
        pass
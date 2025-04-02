from abc import ABC, abstractmethod
from typing import List

from domain.dto.input import OrderInputDTO, OrderDetailInputDTO
from domain.dto.common import DetailedOrderDTO
from domain.dto.context import UserContextDTO

class CreateOrderUseCase(ABC):
    @abstractmethod
    async def create_order(
        self,
        order_input: OrderInputDTO,
        details_input: List[OrderDetailInputDTO],
        context: UserContextDTO
    ) -> DetailedOrderDTO:
        pass

class CreateAdminOrderUseCase(ABC):
    @abstractmethod
    async def create_order(
        self,
        order_input: OrderInputDTO,
        details_input: List[OrderDetailInputDTO],
        context: UserContextDTO
    ) -> DetailedOrderDTO:
        pass
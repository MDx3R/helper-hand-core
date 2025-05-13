from abc import ABC, abstractmethod

from domain.entities.user.contractor.contractor import Contractor


class ContractorOrderQueryRepository(ABC):
    # TODO: Переместить в ContractorQueryRepository
    @abstractmethod
    async def get_contractor(self, order_id: int) -> Contractor | None:
        pass

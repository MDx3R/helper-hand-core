from domain.entities import User, Contractor
from domain.services.user import ContractorUserService

from domain.repositories import UserRepository

from application.transactions import TransactionManager
from application.dtos.output import ContractorOutputDTO, ContracteeOutputDTO

class ContractorUserServiceImpl(ContractorUserService):
    def __init__(
        self, 
        user_repository: UserRepository,
        transaction_manager: TransactionManager,
    ):
        self.user_repository = user_repository
        self.transaction_manager = transaction_manager

    async def get_user(self, user_id: int, contractor: Contractor) -> User | None:
        if user_id == contractor.contractor_id:
            return self.get_profile(contractor)
        
        user = self.user_repository.get_contractee_by_id(user_id)
        if not user:
            return None

        return ContracteeOutputDTO.from_contractee(user)

    async def get_profile(self, contractor: Contractor) -> Contractor:
        return ContractorOutputDTO.from_contractor(contractor)
from domain.entities.base import ApplicationModel
from domain.entities.user.contractee.contractee import Contractee
from domain.entities.user.contractor.contractor import Contractor
from domain.entities.user.credentials import UserCredentials


class CompleteContractee(ApplicationModel):
    contractee: Contractee
    credentials: UserCredentials

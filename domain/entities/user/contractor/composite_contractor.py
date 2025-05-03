from domain.entities.base import ApplicationModel
from domain.entities.user.contractor.contractor import Contractor
from domain.entities.user.credentials import UserCredentials


class CompleteContractor(ApplicationModel):
    contractor: Contractor
    credentials: UserCredentials

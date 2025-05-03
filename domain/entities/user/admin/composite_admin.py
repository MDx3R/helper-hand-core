from typing import Optional
from domain.entities.base import ApplicationModel
from domain.entities.user.admin.admin import Admin
from domain.entities.user.contractor.contractor import Contractor
from domain.entities.user.credentials import UserCredentials


class AdminWithContractor(ApplicationModel):
    admin: Admin
    contractor: Optional[Contractor] = None


class CompleteAdmin(AdminWithContractor):
    credentials: UserCredentials

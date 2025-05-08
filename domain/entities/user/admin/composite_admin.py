from typing import Optional
from domain.entities.base import ApplicationModel
from domain.entities.user.admin.admin import Admin
from domain.entities.user.contractor.contractor import Contractor
from domain.entities.user.credentials import UserCredentials


class AdminWithContractor(ApplicationModel):
    user: Admin
    contractor: Optional[Contractor] = None


class CompleteAdmin(
    AdminWithContractor
):  # TODO: Возможно, не наследовать, а использовать?
    credentials: UserCredentials

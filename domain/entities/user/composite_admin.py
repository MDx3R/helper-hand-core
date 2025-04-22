from domain.entities.base import ApplicationModel
from domain.entities.user.admin import Admin
from domain.entities.user.contractor import Contractor


class AdminWithContractor(ApplicationModel):
    admin: Admin
    contractor: Contractor

from typing import List, Optional

from domain.entities.base import ApplicationModel
from domain.entities.user.admin import Admin
from domain.entities.user.contractor import Contractor

from .detail import OrderDetail
from .order import Order


class OrderWithDetails(ApplicationModel):
    """
    Композитная модель заказа и его сведений.
    """

    order: Order
    details: List[OrderDetail]


class OrderWithDetailsAndContractor(ApplicationModel):
    """
    Композитная модель заказа, его сведений и владельца этого заказа.
    """

    order: Order
    details: List[OrderDetail]
    contractor: Contractor


class OrderWithDetailsAndSupervisor(ApplicationModel):
    """
    Композитная модель заказа, его сведений и куратора этого заказа.
    """

    order: Order
    details: List[OrderDetail]
    admin: Optional[Admin]


class CompleteOrder(ApplicationModel):
    """
    Композитная модель заказа и связанных с ним сущностей.
    """

    order: Order
    details: List[OrderDetail]
    contractor: Contractor
    admin: Optional[Admin]

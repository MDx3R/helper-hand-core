from typing import Type, TypeVar, List
from domain.models import (
    ApplicationModel, 
    User, Admin, Contractee, Contractor,
    Order, OrderDetail, DetailedOrder
)
from infrastructure.database.models import (
    Base, 
    UserBase, AdminBase, ContracteeBase, ContractorBase,
    OrderBase, OrderDetailBase
)

T = TypeVar("T", bound=ApplicationModel)
A = TypeVar("A", bound=User)

def base_to_model(base: Base, model: Type[T]) -> T:
    """Конвертирует SQLAlchemy-модель в модель приложения."""
    return model.model_validate(base.__dict__)

def user_base_to_model(
    user: UserBase,
    role: AdminBase | ContracteeBase | ContractorBase,
    model: Type[A]
) -> A:
    """Конвертирует SQLAlchemy-модель пользователя и его подтип (`AdminBase`, `ContracteeBase`, `ContractorBase`) в модель приложения."""
    user_model = User(**user.__dict__)
    return model(**user_model.model_dump(), **role.__dict__)

def detailed_order_base_to_model(
    order: OrderBase, 
    details: List[OrderDetailBase]
) -> DetailedOrder:
    """Конвертирует SQLAlchemy-модель заказа и его позиций в модель приложения."""
    return DetailedOrder(**order.__dict__, details=[base_to_model(i, OrderDetail) for i in details])

def user_to_base(user: User) -> UserBase:
    """Конвертирует модель пользователя в `UserBase`."""
    return UserBase(
        user_id=user.user_id,
        surname=user.surname,
        name=user.name,
        patronymic=user.patronymic,
        phone_number=user.phone_number,
        role=user.role,
        telegram_id=user.telegram_id,
        chat_id=user.chat_id,
        status=user.status,
        photos=user.photos,
    )

def contractee_to_base(contractee: Contractee) -> ContracteeBase:
    """Конвертирует модель исполнителя в `ContracteeBase`."""
    return ContracteeBase(
        contractee_id=contractee.user_id,
        birthday=contractee.birthday,
        height=contractee.height,
        gender=contractee.gender,
        citizenship=contractee.citizenship,
        positions=contractee.positions,
    )

def contractor_to_base(contractor: Contractor) -> ContractorBase:
    """Конвертирует модель заказчика в `ContractorBase`."""
    return ContractorBase(
        contractor_id=contractor.user_id,
        about=contractor.about,
    )

def admin_to_base(admin: Admin) -> AdminBase:
    """Конвертирует модель администратора в `AdminBase`."""
    return AdminBase(
        admin_id=admin.user_id,
        about=admin.about,
        contractor_id=admin.contractor_id,
    )

def order_to_base(order: Order) -> OrderBase:
    """Конвертирует модель заказа в `OrderBase`."""
    return OrderBase(
        order_id=order.order_id,
        contractor_id=order.contractor_id,
        about=order.about,
        address=order.address,
        admin_id=order.admin_id,
        status=order.status,
    )

def order_detail_to_base(detail: OrderDetail) -> OrderDetailBase:
    """Конвертирует модель позиции заказа в `OrderDetailBase`."""
    return OrderDetailBase(
        detail_id=detail.detail_id,
        order_id=detail.order_id,
        date=detail.date,
        start_at=detail.start_at,
        end_at=detail.end_at,
        position=detail.position,
        count=detail.count,
        wager=detail.wager,
        gender=detail.gender
    )
from datetime import datetime, timedelta
from typing import List, Union, overload

from domain.entities.order.detail import OrderDetail
from domain.entities.order.enums import OrderStatusEnum
from domain.entities.order.order import Order
from domain.entities.reply.available_replies_for_detail import (
    AvailableRepliesForDetail,
)
from domain.entities.reply.enums import ReplyStatusEnum
from domain.entities.reply.reply import Reply
from domain.entities.user.admin.admin import Admin
from domain.entities.user.contractee.contractee import Contractee
from domain.entities.user.enums import RoleEnum, UserStatusEnum
from domain.entities.user.user import User
from domain.time import get_current_time


class UserDomainService:
    @staticmethod
    def is_unverified(user: User) -> bool:
        return user.status == UserStatusEnum.created

    @staticmethod
    def is_pending(user: User) -> bool:
        return user.status == UserStatusEnum.pending

    @staticmethod
    def is_registered(user: User) -> bool:
        return user.status == UserStatusEnum.registered

    @staticmethod
    def is_disapproved(user: User) -> bool:
        return user.status == UserStatusEnum.disapproved

    @staticmethod
    def is_dropped(user: User) -> bool:
        return user.status == UserStatusEnum.dropped

    @staticmethod
    def is_banned(user: User) -> bool:
        return user.status == UserStatusEnum.banned

    @staticmethod
    def is_contractee(user: User) -> bool:
        return user.role == RoleEnum.contractee

    @staticmethod
    def is_contractor(user: User) -> bool:
        return user.role == RoleEnum.contractor

    @staticmethod
    def is_admin(user: User) -> bool:
        return user.role == RoleEnum.admin

    @staticmethod
    def has_role(user: User, *roles) -> bool:
        return any(user.role == role for role in roles)

    @classmethod
    def can_status_be_changed(
        cls, user: User, change_to: UserStatusEnum
    ) -> bool:
        if not cls.is_editable_by_others(user):
            return False
        match change_to:
            case UserStatusEnum.registered:  # approved
                return cls.can_be_approved(user)
            case UserStatusEnum.disapproved:  # disapproved
                return cls.can_be_disapproved(user)
            case UserStatusEnum.dropped:
                return cls.can_be_dropped(user)
            case UserStatusEnum.banned:
                return cls.can_be_banned(user)

        return False

    @classmethod
    def can_be_approved(cls, user: User) -> bool:
        return cls.is_pending(user)

    @classmethod
    def can_be_disapproved(cls, user: User) -> bool:
        return cls.is_pending(user)

    @classmethod
    def can_be_dropped(cls, user: User) -> bool:
        return not cls.is_dropped(user) and not cls.is_admin(user)

    @classmethod
    def can_be_banned(cls, user: User) -> bool:
        return not cls.is_banned(user) and not cls.is_admin(user)

    @classmethod
    def is_editable_by_others(cls, user: User) -> bool:
        """
        Проверяет может ли пользователь быть изменен другими.

        Профили администраторов доступны для редактирования только владельцу этого профиля.
        """
        return not cls.is_admin(user)

    @classmethod
    def is_allowed_to_register(cls, user: User) -> bool:
        return cls.is_dropped(user) or cls.is_disapproved(user)


class AdminDomainService:
    @staticmethod
    def is_contractor(admin: Admin) -> bool:
        return admin.contractor_id is not None


class OrderDomainService:
    @staticmethod
    def is_owned_by(order: Order, contractor_id: int) -> bool:
        return contractor_id == order.contractor_id

    @staticmethod
    def is_supervised_by(order: Order, user_id: int) -> bool:
        return user_id == order.supervisor_id

    @staticmethod
    def has_supervisor(order: Order) -> bool:
        return order.supervisor_id is not None

    @staticmethod
    def is_created(order: Order) -> bool:
        return order.status == OrderStatusEnum.created

    @staticmethod
    def is_open(order: Order) -> bool:
        return order.status == OrderStatusEnum.open

    @staticmethod
    def is_closed(order: Order) -> bool:
        return order.status == OrderStatusEnum.closed

    @staticmethod
    def is_active(order: Order) -> bool:
        return order.status == OrderStatusEnum.active

    @staticmethod
    def is_cancelled(order: Order) -> bool:
        return order.status == OrderStatusEnum.cancelled

    @staticmethod
    def is_fulfilled(order: Order) -> bool:
        return order.status == OrderStatusEnum.fulfilled

    @classmethod
    def is_available(cls, order: Order) -> bool:
        return cls.is_open(order)

    @classmethod
    def can_be_assigned(cls, order: Order) -> bool:
        return not cls.has_supervisor(order) and cls.is_created(order)

    @classmethod
    def can_be_approved(cls, order: Order) -> bool:
        """
        Проверяет как и возможность подтвердить заказ (`approve`),
        так и отменить (`disapprove`)
        """
        return cls.is_created(order)

    @classmethod
    def can_status_be_changed(
        cls, order: Order, change_to: OrderStatusEnum
    ) -> bool:
        match change_to:
            case OrderStatusEnum.open:
                return cls.can_be_opened(order)
            case OrderStatusEnum.cancelled:
                return cls.can_be_cancelled(order)
            case OrderStatusEnum.closed:
                return cls.can_be_closed(order)
            case OrderStatusEnum.active:
                return cls.can_be_set_active(order)
            case OrderStatusEnum.fulfilled:
                return cls.can_be_fulfilled(order)

        return False

    @classmethod
    def can_be_cancelled(cls, order: Order) -> bool:
        return not cls.is_fulfilled(order) and not cls.is_cancelled(order)

    @classmethod
    def can_be_closed(cls, order: Order) -> bool:
        return cls.is_open(order)

    @classmethod
    def can_be_opened(cls, order: Order) -> bool:
        return cls.is_closed(order)

    @classmethod
    def can_be_set_active(cls, order: Order) -> bool:
        return cls.is_open(order) or cls.is_closed(order)

    @classmethod
    def can_be_fulfilled(cls, order: Order) -> bool:
        return cls.is_active(order)

    @classmethod
    def can_have_replies(cls, order: Order) -> bool:
        return cls.is_open(order)


class OrderDetailDomainService:
    starts_after = timedelta(hours=2)
    max_lenght = timedelta(hours=20)

    @staticmethod
    def is_suitable(detail: OrderDetail, contractee: Contractee) -> bool:
        return not detail.gender or detail.gender == contractee.gender

    @classmethod
    def is_relevant_at_current_time(cls, detail: OrderDetail) -> bool:
        return detail.start_at - cls.starts_after > get_current_time()

    @classmethod
    def get_latest_allowed_start_time(cls) -> datetime:
        """
        Получает такое минимальное время,
        что для любой позиции, заканчивающейся после настоящего времени,
        время начала всегда больще полученного времени.
        """
        return get_current_time() - cls.max_lenght


class ReplyDomainService:
    @staticmethod
    def is_created(reply: Reply) -> bool:
        return reply.status == ReplyStatusEnum.created

    @staticmethod
    def is_accepted(reply: Reply) -> bool:
        return reply.status == ReplyStatusEnum.accepted

    @staticmethod
    def is_disapproved(reply: Reply) -> bool:
        return reply.status == ReplyStatusEnum.accepted

    @staticmethod
    def is_paid(reply: Reply) -> bool:
        return reply.status == ReplyStatusEnum.paid

    @staticmethod
    def is_dropped(reply: Reply) -> bool:
        return reply.dropped

    @classmethod
    def is_future(cls, reply: Reply, detail: OrderDetail) -> bool:
        return (
            cls.is_future_or_ongoing(reply, detail)
            and detail.start_date > get_current_time()
        )

    @classmethod
    def is_future_or_ongoing(cls, reply: Reply, detail: OrderDetail) -> bool:
        return (
            not reply.dropped
            and cls.is_accepted(reply)
            and detail.end_date > get_current_time()
        )

    @classmethod
    def can_be_approved(cls, reply: Reply) -> bool:
        return cls.is_created(reply)

    @classmethod
    def can_be_dropped(cls, reply: Reply) -> bool:
        return cls.is_created(reply)


class AvailabilityDomainService:
    @staticmethod
    def is_full(availability: AvailableRepliesForDetail) -> bool:
        return availability.quantity <= 0

    @classmethod
    def are_all_full(
        cls, availabilities: List[AvailableRepliesForDetail]
    ) -> bool:
        return all(cls.is_full(av) for av in availabilities)

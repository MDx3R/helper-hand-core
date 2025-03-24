import enum

"""
Этот модуль содержит перечисления для моделей.
"""

class RoleEnum(str, enum.Enum):
    """
    Возможные роли пользователя.
    """
    admin = "admin"
    developer = "developer" 
    contractor = "contractor" 
    contractee = "contractee"

class UserStatusEnum(str, enum.Enum):
    """
    Возможные статусы пользователя.
    """
    created = "created" # Статус, устанавливаемый при создании пользователя
    pending = "pending"  # Статус, устанавливаемый при создании заявки на регистрацию.
    registered = "registered"  # Статус, устанавливаемый после подтверждения регистрации.
    dropped = "dropped"  # Статус, означающий, что регистрация была сброшена, но данные о пользователе сохранились.
    banned = "banned"  # Статус, означающий, что пользователь был заблокирован.

class OrderStatusEnum(str, enum.Enum):
    """
    Возможные статусы заказа.
    """
    created = "created" # Статус, устанавливаемый при создании заказа
    open = "open" # Статус, устанавливаемый для активных заказов: этот статус подразумевает, что на заказ можно откликнуться
    closed = "closed" # Статус, означающий, что заказ находится в закрытом состоянии - на него нельзя откликнуться.
    active = "active" # Статус, означающий, что заказ находится в работе
    cancelled = "cancelled" # Статус, устанавливаемый для отмененных заказов
    fulfilled = "fulfilled" # Статус, устанавливаемый для завершенных заказов

class ReplyStatusEnum(str, enum.Enum):
    """
    Возможные статусы отклика на заказ.
    """
    created = "created" # Статус, устанавливаемый при создании отклика
    accepted = "accepted" # Статус, означающий, что отклик был подтвержден
    dropped = "dropped" # Статус, означающий, что отклик был отменен
    paid = "paid" # Статус, устанавливаемый при проведенной оплате по заказу

class GenderEnum(str, enum.Enum):
    male = "Мужской"
    female = "Женский"

class CitizenshipEnum(str, enum.Enum):
    """
    Возможные варианты гражданства
    """
    russia = "Российское"
    other = "Другое"

class PositionEnum(str, enum.Enum):
    """
    Возможные варианты позиций для заказа.
    """
    helper = "Хелпер"
    hostess = "Хостес"
    installer = "Монтажник"
    parking = "Парковщик"
    other = "Другая"
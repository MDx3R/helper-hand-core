import enum


class RoleEnum(str, enum.Enum):
    unset = "unset"
    admin = "admin"
    developer = "developer"
    contractor = "contractor"
    contractee = "contractee"


class UserStatusEnum(str, enum.Enum):
    created = "created"  # Статус, устанавливаемый при создании пользователя
    pending = "pending"  # Статус, устанавливаемый при создании заявки на регистрацию.
    registered = "registered"  # Статус, устанавливаемый после подтверждения регистрации.
    disapproved = "disapproved"  # Статус, устанавливаемый после отказа в прохождении регистрации
    dropped = "dropped"  # Статус, означающий, что регистрация была сброшена, но данные о пользователе сохранились
    banned = "banned"  # Статус, означающий, что пользователь был заблокирован

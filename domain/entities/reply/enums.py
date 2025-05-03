import enum


class ReplyStatusEnum(str, enum.Enum):
    """
    Возможные статусы отклика на заказ.
    """

    created = "created"  # Статус, устанавливаемый при создании отклика
    accepted = "accepted"  # Статус, означающий, что отклик был подтвержден
    disapproved = "disapproved"  # Статус, означающий, что отклик был отклонен
    paid = "paid"  # Статус, устанавливаемый при проведенной оплате по заказу

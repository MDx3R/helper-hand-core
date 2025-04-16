import enum

"""
Этот модуль содержит общие перечисления для моделей.
"""


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

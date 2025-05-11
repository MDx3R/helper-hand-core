import enum


class TokenTypeEnum(str, enum.Enum):
    access = "access"
    refresh = "refresh"

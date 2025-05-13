from datetime import date, datetime, time
from typing import Any, List, Optional

from sqlalchemy import BigInteger, ForeignKey, Integer, String, func, text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from domain.entities.enums import (
    CitizenshipEnum,
    GenderEnum,
    PositionEnum,
)
from domain.entities.order.enums import OrderStatusEnum
from domain.entities.reply.enums import ReplyStatusEnum
from domain.entities.token.enums import TokenTypeEnum
from domain.entities.user.enums import RoleEnum, UserStatusEnum


class Base(DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    def get_fields(self) -> dict[str, Any]:
        return {
            column: getattr(self, column)
            for column in self._get_column_names()
        }

    @classmethod
    def _get_column_names(cls) -> set[str]:
        return {column.name for column in cls.__table__.columns}

    @classmethod
    def _filter_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        return {k: v for k, v in data.items() if k in cls._get_column_names()}

    @classmethod
    def base_validate(cls, data: dict[str, Any]) -> "Base":
        return cls(**cls._filter_fields(data))


class UserBase(Base):
    __tablename__ = "User"

    user_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    surname: Mapped[str]
    name: Mapped[str]
    patronymic: Mapped[str | None]
    phone_number: Mapped[str] = mapped_column(String, unique=True)
    role: Mapped[RoleEnum]
    status: Mapped[UserStatusEnum]
    photos: Mapped[List[str]] = mapped_column(ARRAY(String))


class AdminBase(Base):
    __tablename__ = "Admin"

    admin_id: Mapped[int] = mapped_column(
        ForeignKey("User.user_id"), primary_key=True
    )
    about: Mapped[str]
    contractor_id: Mapped[int | None]


class ContracteeBase(Base):
    __tablename__ = "Contractee"

    contractee_id: Mapped[int] = mapped_column(
        ForeignKey("User.user_id"), primary_key=True
    )
    birthday: Mapped[date]
    height: Mapped[int]
    gender: Mapped[GenderEnum]
    citizenship: Mapped[CitizenshipEnum]
    positions: Mapped[List[PositionEnum]] = mapped_column(ARRAY(String))


class ContractorBase(Base):
    __tablename__ = "Contractor"

    contractor_id: Mapped[int] = mapped_column(
        ForeignKey("User.user_id"), primary_key=True
    )
    about: Mapped[str]


class OrderBase(Base):
    __tablename__ = "Order"

    order_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    contractor_id: Mapped[int] = mapped_column(
        ForeignKey("Contractor.contractor_id")
    )
    about: Mapped[str]
    address: Mapped[str]
    admin_id: Mapped[int | None] = mapped_column(ForeignKey("Admin.admin_id"))
    status: Mapped[OrderStatusEnum] = mapped_column(
        server_default=text(f"'{OrderStatusEnum.created.value}'")
    )


class OrderDetailBase(Base):
    __tablename__ = "OrderDetail"

    detail_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    order_id: Mapped[int] = mapped_column(ForeignKey("Order.order_id"))
    date: Mapped[date]
    start_at: Mapped[time]
    end_at: Mapped[time]
    position: Mapped[PositionEnum]
    count: Mapped[int]
    wager: Mapped[int]
    fee: Mapped[int]
    gender: Mapped[GenderEnum | None]


class ReplyBase(Base):
    __tablename__ = "Reply"

    reply_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    contractee_id: Mapped[int] = mapped_column(
        ForeignKey("Contractee.contractee_id"), primary_key=True
    )
    detail_id: Mapped[int] = mapped_column(
        ForeignKey("OrderDetail.detail_id"), primary_key=True
    )
    wager: Mapped[int]
    status: Mapped[ReplyStatusEnum] = mapped_column(
        server_default=text(f"'{ReplyStatusEnum.created.value}'")
    )
    dropped: Mapped[bool] = mapped_column(server_default=text("false"))
    paid: Mapped[datetime | None]


class WebCredentialsBase(Base):
    __tablename__ = "WebCredentials"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("User.user_id"), primary_key=True
    )
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str]


class TelegramCredentialsBase(Base):
    __tablename__ = "TelegramCredentials"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("User.user_id"), primary_key=True
    )
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True)


class TokenBase(Base):
    __tablename__ = "Token"

    token_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("User.user_id"))
    token: Mapped[str] = mapped_column(String, unique=True)
    type: Mapped[TokenTypeEnum]
    revoked: Mapped[bool] = mapped_column(server_default=text("false"))
    expires_at: Mapped[datetime]

from typing import List, Optional, Any

from datetime import datetime, time

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

from sqlalchemy import (
    func, 
    text,
    ForeignKey,
    String,
    Integer,
    BigInteger, 
    String, 
)

from sqlalchemy.dialects.postgresql import ARRAY

from domain.models.enums import (
    RoleEnum,
    UserStatusEnum,
    GenderEnum,
    CitizenshipEnum,
    PositionEnum,
    OrderStatusEnum,
    ReplyStatusEnum
)

class Base(DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    def get_fields(self) -> dict[str, Any]:
        return {column: getattr(self, column) for column in self._get_column_names()}

    @classmethod
    def _get_column_names(cls) -> set[str]:
        return {column.name for column in cls.__table__.columns}

    @classmethod
    def _filter_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        return {k: v for k, v in data.items() if k in cls._get_column_names()}

    @classmethod
    def base_validate(cls, data: dict[str, Any]) -> 'Base':
        return cls(**cls._filter_fields(data))

class UserBase(Base):
    __tablename__ = "User"
    
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    surname: Mapped[str]
    name: Mapped[str]
    patronymic: Mapped[str | None]
    phone_number: Mapped[str]
    role: Mapped[RoleEnum]
    status: Mapped[UserStatusEnum]
    photos: Mapped[List[str]] = mapped_column(ARRAY(String))

    # Будет перемещено в отдельное отношение TelegramUser
    # На данный момент telegram_id выступает в роли Primary Key, хотя таковым не является: предусматривается, что пользователь может быть не только TelegramUser.
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True)

class AdminBase(Base):
    __tablename__ = "Admin"
    
    admin_id: Mapped[int] = mapped_column(ForeignKey("User.user_id"), primary_key=True)
    about: Mapped[str]
    contractor_id: Mapped[int | None]

class ContracteeBase(Base):
    __tablename__ = "Contractee"
    
    contractee_id: Mapped[int] = mapped_column(ForeignKey("User.user_id"), primary_key=True)
    birthday: Mapped[datetime]
    height: Mapped[int]
    gender: Mapped[GenderEnum]
    citizenship: Mapped[CitizenshipEnum]
    positions: Mapped[List[PositionEnum]] = mapped_column(ARRAY(String))

class ContractorBase(Base):
    __tablename__ = "Contractor"
    
    contractor_id: Mapped[int] = mapped_column(ForeignKey("User.user_id"), primary_key=True)
    about: Mapped[str]

class OrderBase(Base):
    __tablename__ = "Order"
    
    order_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    contractor_id: Mapped[int] = mapped_column(ForeignKey("Contractor.contractor_id"))
    about: Mapped[str]
    address: Mapped[str]
    admin_id: Mapped[int | None] = mapped_column(ForeignKey("Admin.admin_id"))
    status: Mapped[OrderStatusEnum] = mapped_column(server_default=text(f"'{OrderStatusEnum.created.value}'"))

class OrderDetailBase(Base):
    __tablename__ = "OrderDetail"
    
    detail_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("Order.order_id"))
    date: Mapped[datetime]
    start_at: Mapped[time]
    end_at: Mapped[time]
    position: Mapped[PositionEnum]
    count: Mapped[int]
    wager: Mapped[int]
    gender: Mapped[GenderEnum | None]

class ReplyBase(Base):
    __tablename__ = "Reply"
    
    contractee_id: Mapped[int] = mapped_column(ForeignKey("Contractee.contractee_id"), primary_key=True)
    detail_id: Mapped[int] = mapped_column(ForeignKey("OrderDetail.detail_id"), primary_key=True)
    wager: Mapped[int]
    status: Mapped[ReplyStatusEnum] = mapped_column(server_default=text(f"'{ReplyStatusEnum.created.value}'"))
    paid: Mapped[datetime | None]
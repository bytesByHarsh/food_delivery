# Built-in Dependencies
from typing import Optional
from uuid import UUID

# Third-Party Dependencies
from sqlmodel import Field, Relationship
from enum import Enum

# Local Dependencies
from app.db.models.v1.common import (
    SoftDeleteMixin,
    TimestampMixin,
    UUIDMixin,
    Base,
)
from app.core.config import settings

class UserAddressType_Enum(str, Enum):
    HOME = "home"
    OFFICE = "office"
    OTHER = "other"

class UserAddressLocation(Base):
    latitude: float = Field(
        default= 0.0,
        nullable= False,
        description="Latitude coordinate of the address"
    )
    longitude: float = Field(
        default= 0.0,
        nullable= False,
        description="Longitude coordinate of the address"
    )

class UserAddressBase(Base):
    address_line_1: str = Field(
        default="",
        nullable=True
    )
    address_line_2: Optional[str] = Field(
        default=None,
        nullable=False
    )
    city: str= Field(
        default="",
        nullable=True
    )
    state: str= Field(
        default="",
        nullable=True
    )
    postal_code: str= Field(
        default="",
        nullable=True
    )
    country: str= Field(
        default="",
        nullable=True
    )

    add_type: UserAddressType_Enum = Field(
        default= UserAddressType_Enum.OTHER,
        nullable=False
    )

    customer_id: UUID = Field(foreign_key=f"{settings.DATABASE_USER_TABLE}.id")

class UserAddressUserDetails(Base):
    customer = Relationship(back_populates="user_addresses")


class UserAddress(
    UserAddressBase,
    UserAddressUserDetails,
    UserAddressLocation,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    table=True
):
    __tablename__ = f"{settings.DATABASE_USER_ADDRESS_TABLE}"
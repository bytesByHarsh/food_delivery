# Built-in Dependencies
from typing import List

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

class RestaurantInfoBase(Base):
    name:str = Field(
        min_length=2,
        max_length=100,
        nullable=False,
        description="Restaurant's full name",
        schema_extra={"examples": ["Test Restaurant"]},
    )
    address:str = Field(nullable=False, default="", index=False)
    open_hr:int = Field(nullable=False, default=10, index=False)
    close_hr:int = Field(nullable=False, default=23, index=False)
    latitude:float = Field(nullable=False, default=0.0, index=False)
    longitude:float = Field(nullable=False, default=0.0, index=False)
    pincode:int = Field(nullable=False, default=0, index=False)

class RestaurantPermissionBase(Base):
    is_superuser: bool = Field(
        default=False, description="Indicates whether the restaurant has superuser privileges"
    )

class RestaurantSecurityBase(Base):
    hashed_password: str = Field(
        nullable=False, description="Hashed password for restaurant authentication"
    )

class RestaurantLoginInfoBase(Base):
    username:str = Field(
        min_length=2,
        max_length=20,
        unique=True,
        index=True,
        nullable=False,
        regex=r"^[a-z0-9]+$",
        description="User's username",
        schema_extra={"examples": ["test"]},
    )
    email:str = Field(
        max_length=50,
        unique=True,
        index=True,
        nullable=False,
        regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        description="User's email address",
        schema_extra={"examples": ["test@example.com"]},
    )
    phone:str = Field(
        unique=True,
        index=True,
        nullable=False,
        regex=r"^\+?[1-9]\d{1,14}$",
        description="Phone number in international format, e.g., +919876543210",
        schema_extra={"examples": ["+919876543210"]},
    )



class RestaurantRelation(Base):
    menu_items = Relationship(back_populates="restaurant")

class Restaurant(
    RestaurantInfoBase,
    RestaurantPermissionBase,
    RestaurantSecurityBase,
    RestaurantLoginInfoBase,
    RestaurantRelation,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    table=True,
):
    __tablename__ = f"{settings.DATABASE_RESTAURANT_TABLE}"
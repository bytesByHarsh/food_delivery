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
    name:str = Field(nullable=False, default="Dummy Restaurant", index=False)
    address:str = Field(nullable=False, default="", index=False)
    open_hr:int = Field(nullable=False, default=10, index=False)
    close_hr:int = Field(nullable=False, default=23, index=False)
    latitude:float = Field(nullable=False, default=0.0, index=False)
    longitude:float = Field(nullable=False, default=0.0, index=False)
    pincode:int = Field(nullable=False, default=0, index=False)


class RestaurantRelation(Base):
    menu_items = Relationship(back_populates="restaurant")

class Restaurant(
    RestaurantInfoBase,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    table=True,
):
    __tablename__ = f"{settings.DATABASE_RESTAURANT_TABLE}"
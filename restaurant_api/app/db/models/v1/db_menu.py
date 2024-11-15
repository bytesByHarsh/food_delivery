# Built-in Dependencies
from typing import List
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

class ItemAddOnBaseInfo(Base):
    name:str = Field(nullable=False, default="", index=False)
    description:str = Field(nullable=False, default="", index=False)
    price:float = Field(nullable=False, default=0.0, index=False)
    available:bool = Field(nullable=False, default=True, index=False)
class ItemAddOnRelation(Base):
    item_id:UUID = Field(nullable=False, index=True, foreign_key=f"{settings.DATABASE_MENU_ITEM_TABLE}.id")
    item = Relationship(back_populates="add_ons")

class ItemAddOn(
    ItemAddOnBaseInfo,
    ItemAddOnRelation,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    table=True,
):
    __tablename__ = f"{settings.DATABASE_MENU_ITEM_ADDON_TABLE}"

class MenuItemBaseInfo(Base):
    name:str = Field(nullable=False, default="", index=False)
    description:str = Field(nullable=False, default="", index=False)
    price:float = Field(nullable=False, default=0.0, index=False)
    available:bool = Field(nullable=False, default=True, index=False)

class MenuItemRelation(Base):
    restaurant_id:UUID = Field(nullable=False, index=False, foreign_key=f"{settings.DATABASE_RESTAURANT_TABLE}.id")
    restaurant = Relationship(back_populates="menu_items")
    add_ons = Relationship(back_populates="item")

class MenuItem(
    MenuItemBaseInfo,
    MenuItemRelation,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    table=True,
):
    __tablename__ = f"{settings.DATABASE_MENU_ITEM_TABLE}"



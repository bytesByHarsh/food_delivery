# Built-in Dependencies
from typing import Annotated, List
from datetime import datetime

# Third-Party Dependencies
from pydantic import BaseModel, Field, ConfigDict

# Local Dependencies
from app.db.models.v1.common import UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.utils.partial import optional

from app.db.models.v1.db_menu import (
    ItemAddOnBaseInfo,
    ItemAddOnRelation,

    MenuItemBaseInfo,
    MenuItemRelation,
)

class MenuItemBase(
    MenuItemBaseInfo,
    MenuItemRelation
):
    pass

class MenuItem(
    MenuItemBase,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
):
    pass

class MenuItemRead(
    MenuItemBase
):
    pass

class MenuItemCreate(
    MenuItemBase
):
    model_config = ConfigDict(extra="forbid")  # type: ignore

class MenuItemCreateInternal(
    MenuItemBase,
):
    pass

@optional
class MenuItemUpdate(
    MenuItemBaseInfo
):
    class Config:
        extra = "forbid"

class MenuItemUpdateInternal(MenuItemUpdate):
    updated_at: datetime

class MenuItemDelete(SoftDeleteMixin):
    class Config:
        extra = "forbid"

class MenuItemRestoreDeleted(BaseModel):
    is_deleted: bool


class ItemAddOnBase(
    ItemAddOnBaseInfo,
    ItemAddOnRelation
):
    pass

class ItemAddOn(
    ItemAddOnBase,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
):
    pass

class ItemAddOnRead(
    ItemAddOnBase
):
    pass

class ItemAddOnCreate(
    ItemAddOnBase
):
    model_config = ConfigDict(extra="forbid")  # type: ignore

class ItemAddOnCreateInternal(
    ItemAddOnBase,
):
    pass

@optional
class ItemAddOnUpdate(
    ItemAddOnBaseInfo
):
    class Config:
        extra = "forbid"

class ItemAddOnUpdateInternal(ItemAddOnUpdate):
    updated_at: datetime

class ItemAddOnDelete(SoftDeleteMixin):
    class Config:
        extra = "forbid"

class ItemAddOnRestoreDeleted(BaseModel):
    is_deleted: bool
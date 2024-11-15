# Built-in Dependencies
from typing import Annotated, List
from datetime import datetime

# Third-Party Dependencies
from pydantic import BaseModel, Field, ConfigDict

# Local Dependencies
from app.db.models.v1.common import UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.utils.partial import optional
from app.db.models.v1.db_restaurant import (
    RestaurantInfoBase,
    RestaurantPermissionBase,
    RestaurantSecurityBase,
    RestaurantLoginInfoBase,
    RestaurantRelation,
)

class RestaurantBase(
    RestaurantInfoBase,
):
    pass

class Restaurant(
    RestaurantBase,
    RestaurantPermissionBase,
    RestaurantSecurityBase,
    RestaurantLoginInfoBase,
    RestaurantRelation,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
):
    pass

class RestaurantRead(
    RestaurantLoginInfoBase,
    RestaurantRelation,
    UUIDMixin,
):
    pass

class RestaurantCreate(
    RestaurantBase,
    RestaurantLoginInfoBase,
):
    model_config = ConfigDict(extra="forbid")  # type: ignore

    password: Annotated[
        str,
        Field(
            default="Pass@123",
            pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$",
            examples=["Str1ngst!"],
        ),
    ]

class RestaurantCreateInternal(
    RestaurantBase,
    RestaurantLoginInfoBase,
    RestaurantPermissionBase,
    RestaurantSecurityBase
):
    pass

@optional()
class RestaurantUpdate(
    RestaurantBase,
    RestaurantLoginInfoBase,
):
    class Config:
        extra = "forbid"

class RestaurantUpdateInternal(RestaurantUpdate):
    updated_at: datetime

class RestaurantDelete(SoftDeleteMixin):
    class Config:
        extra = "forbid"

class RestaurantRestoreDeleted(BaseModel):
    is_deleted: bool
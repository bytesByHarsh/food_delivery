# Built-in Dependencies
from typing import Annotated, List
from datetime import datetime

# Third-Party Dependencies
from pydantic import BaseModel, Field, ConfigDict

# Local Dependencies
from app.db.models.v1.common import UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.utils.partial import optional

from app.db.models.v1.db_order import (
    OrderAddOnBaseInfo,
    OrderItemBaseInfo,
    OrderBaseInfo,
    OrderBaseDeliveryBaseInfo,
    OrderStatusInfo,
    OrderPaymentDetails
)

class OrderAddOnBase(OrderAddOnBaseInfo):
    pass

class OrderAddOn(
    OrderAddOnBase,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
):
    pass

class OrderAddOnRead(OrderAddOnBase, UUIDMixin):
    pass

class OrderAddOnCreate(
    OrderAddOnBase,
):
    class Config:
        extra = "forbid"

class OrderAddOnCreateInternal(
    OrderAddOnBase,
):
    pass

@optional()
class OrderAddOnUpdate(
    OrderAddOnBase,
):
    class Config:
        extra = "forbid"

class OrderAddOnUpdateInternal(
    OrderAddOnBase,
):
    updated_at: datetime


class OrderAddOnDelete(SoftDeleteMixin):
    model_config = ConfigDict(extra="forbid")  # type: ignore

class OrderAddOnRestoreDeleted(BaseModel):
    is_deleted: bool

## Order Item
class OrderItemBase(OrderItemBaseInfo):
    pass

class OrderItem(
    OrderItemBase,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
):
    pass

class OrderItemRead(OrderItemBase, UUIDMixin):
    pass


class OrderItemCreate(
    OrderItemBase,
):
    add_ons: List[OrderAddOnCreate] = Field(default=[OrderAddOnCreate()])
    class Config:
        extra = "forbid"


class OrderItemCreateInternal(
    OrderItemBase,
):
    pass


@optional()
class OrderItemUpdate(
    OrderItemBase,
):
    class Config:
        extra = "forbid"


class OrderItemUpdateInternal(
    OrderItemBase,
):
    updated_at: datetime


class OrderItemDelete(SoftDeleteMixin):
    model_config = ConfigDict(extra="forbid")  # type: ignore


class OrderItemRestoreDeleted(BaseModel):

    is_deleted: bool

## Order
class OrderBase(OrderBaseInfo):
    pass

class Order(
    OrderBase,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
):
    pass

class OrderRead(
    OrderBase,
    UUIDMixin,
    OrderBaseDeliveryBaseInfo,
    OrderStatusInfo,
    OrderPaymentDetails
):
    pass


class OrderCreate(
    OrderBase,
):
    items: List[OrderItemCreate] = Field(default=[])
    class Config:
        extra = "forbid"


class OrderCreateInternal(
    OrderBase,
):
    pass


@optional()
class OrderUpdate(
    OrderBase,
):
    class Config:
        extra = "forbid"


class OrderUpdateInternal(
    OrderBase,
    OrderBaseDeliveryBaseInfo,
    OrderStatusInfo,
    OrderPaymentDetails
):
    updated_at: datetime


class OrderDelete(SoftDeleteMixin):
    model_config = ConfigDict(extra="forbid")  # type: ignore


class OrderRestoreDeleted(BaseModel):

    is_deleted: bool
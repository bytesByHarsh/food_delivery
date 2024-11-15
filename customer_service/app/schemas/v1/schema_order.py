# Built-in Dependencies
from typing import List
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
    OrderPaymentDetails,
    OrderItemRelations,
    OrderAddOnRelation,
)


class OrderAddOnBase(OrderAddOnBaseInfo):
    pass


class OrderAddOn(
    OrderAddOnBase,
    OrderAddOnRelation,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
):
    pass


class OrderAddOnRead(OrderAddOnBase, OrderAddOnRelation, UUIDMixin):
    pass


class OrderAddOnCreate(
    OrderAddOnBase,
):
    class Config:
        extra = "forbid"


class OrderAddOnCreateInternal(OrderAddOnBase, OrderAddOnRelation):
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
    OrderItemRelations,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
):
    pass


class OrderItemRead(OrderItemBase, OrderItemRelations, UUIDMixin):
    pass


class OrderItemCreate(
    OrderItemBase,
):
    add_ons: List[OrderAddOnCreate] = Field(default=[])

    class Config:
        extra = "forbid"


class OrderItemCreateInternal(OrderItemBase, OrderItemRelations):
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
    OrderPaymentDetails,
):
    items: list = []
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
    OrderBase, OrderBaseDeliveryBaseInfo, OrderStatusInfo, OrderPaymentDetails
):
    updated_at: datetime


class OrderDelete(SoftDeleteMixin):
    model_config = ConfigDict(extra="forbid")  # type: ignore


class OrderRestoreDeleted(BaseModel):
    is_deleted: bool


class OrderUpdateDriverDetails(OrderBaseDeliveryBaseInfo):
    model_config = ConfigDict(extra="forbid")  # type: ignore
# Built-in Dependencies
from typing import Optional, List
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
    Rating_enum
)
from app.core.config import settings
# from app.db.models.v1.db_address import UserAddress

class OrderAddOnBaseInfo(Base):
    name: str = Field(nullable=False, default="")
    price: float = Field(nullable=False, default=0.0)
    order_item_id: UUID = Field(nullable=False, index= True)


class OrderAddOn(
    OrderAddOnBaseInfo,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    table=True,
):
    # order_item: "OrderItem" = Relationship(back_populates="add_ons", sa_relationship=True)
    __tablename__ = f"{settings.DATABASE_ORDER_ITEM_ADDON_TABLE}"

class OrderItemBaseInfo(Base):
    order_id: UUID = Field(nullable=False, index= True)
    product_id: UUID = Field(nullable=False, index= False)
    payment_id: UUID = Field(nullable=True, index= False)
    name: str = Field(nullable=False, default="")
    quantity:int = Field(nullable=False, default=1)
    price_per_unit:float = Field(nullable=False, default=0.0)

    # add_ons: List["OrderAddOn"] = Relationship(back_populates="order_item", cascade_delete=True, sa_relationship=True)

class OrderItem(
    OrderItemBaseInfo,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    table=True,
):

    # order: "Order" = Relationship(back_populates="items", sa_relationship=True)
    __tablename__ = f"{settings.DATABASE_ORDER_ITEM_TABLE}"

class Order_Status_Enum(str, Enum):
    PLACED = "placed"
    ORDERED = "ordered"
    ACCEPTED = "accepted"
    ON_THE_WAY = "on_the_way"
    REACHED = "reached"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"
    FAILED = "failed"


class OrderBaseInfo(Base):
    customer_id: UUID = Field(nullable=False, index= True)

    status: Order_Status_Enum = Field(nullable=False, index= False, default=Order_Status_Enum.ORDERED)
    food_rating: Rating_enum = Field(nullable=True, index= False, default=None)

    delivery_rating: Rating_enum = Field(nullable=True, index= False, default=None)
    delivery_person_id:UUID = Field(nullable=True, index= False, default=None)

    address_id :UUID = Field(nullable=False, index=False, foreign_key=f"{settings.DATABASE_USER_ADDRESS_TABLE}.id")

    # items: List[OrderItem] = Relationship(back_populates="order" , cascade_delete=True, sa_relationship=True)
    # delivery_address: "UserAddress" = Relationship(back_populates="orders", sa_relationship=True)


class Order(
    OrderBaseInfo,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    table=True,
):
    __tablename__ = f"{settings.DATABASE_ORDER_TABLE}"
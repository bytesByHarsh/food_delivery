# Built-in Dependencies
from datetime import datetime

# Third-Party Dependencies
from pydantic import BaseModel, ConfigDict

# Local Dependencies
from app.db.models.v1.common import UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.utils.partial import optional
from app.db.models.v1.db_address import (
    UserAddressInfoBase,
    UserAddressLocation,
    UserAddressUserDetails,
)


class UserAddressBase(UserAddressInfoBase, UserAddressLocation):
    pass


class UserAddress(
    UserAddressInfoBase,
    UserAddressUserDetails,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
):
    pass


class UserAddressRead(UserAddressBase, UUIDMixin):
    pass


class UserAddressCreate(
    UserAddressBase,
):
    class Config:
        extra = "forbid"


class UserAddressCreateInternal(
    UserAddressBase,
):
    pass


@optional()
class UserAddressUpdate(
    UserAddressBase,
):
    class Config:
        extra = "forbid"


class UserAddressUpdateInternal(
    UserAddressBase,
):
    updated_at: datetime


class UserAddressDelete(SoftDeleteMixin):
    model_config = ConfigDict(extra="forbid")  # type: ignore


class UserAddressRestoreDeleted(BaseModel):
    """
    API Schema

    Description:
    ----------
    Schema for restoring a deleted user address.

    Fields:
    ----------
    - 'is_deleted': Flag indicating whether the user address record is deleted (soft deletion).
    """

    is_deleted: bool

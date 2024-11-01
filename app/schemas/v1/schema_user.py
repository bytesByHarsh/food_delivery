# Built-in Dependencies
from typing import Annotated
from datetime import datetime

# Third-Party Dependencies
from pydantic import BaseModel, Field, ConfigDict

# Local Dependencies
from app.db.models.v1.common import UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.utils.partial import optional
from app.db.models.v1.db_user import (
    UserPersonalInfoBase,
    UserMediaBase,
    UserPermissionBase,
    UserRoleBase,
    UserSecurityBase,
)


class UserBase(UserPersonalInfoBase):
    """
    API Schema

    Description:
    ----------
    Base schema for representing a user personal info.

    Fields:
    ----------
    - 'name': User's full name.
    - 'username': User's unique username.
    - 'email': User's unique email address.
    """

    pass


class User(
    UserBase,
    UserMediaBase,
    UserPermissionBase,
    UserSecurityBase,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
):
    """
    API Schema

    Description:
    ----------
    Schema representing a user, including media, tier, permission, and security information.

    Fields:
    ----------
    - 'name': User's full name.
    - 'username': User's unique username.
    - 'email': User's unique email address.
    - 'profile_image_url': URL of the user's profile image.
    - 'is_superuser': Indicates whether the user has superuser privileges.
    - 'hashed_password': Hashed password for user authentication.
    - 'id': Unique identifier (UUID) for the user.
    - 'created_at': Timestamp for the creation of the user record.
    - 'updated_at': Timestamp for the last update of the user record.
    - 'deleted_at': Timestamp for the deletion of the user record (soft deletion).
    - 'is_deleted': Flag indicating whether the user record is deleted (soft deletion).
    """

    pass


class UserRead(
    UserBase,
    UserMediaBase,
    UserRoleBase,
    UUIDMixin,
):
    """
    API Schema

    Description:
    ----------
    Read-only schema for retrieving information about a user, including media and tier details.

    Fields:
    ----------
    - 'name': User's full name.
    - 'username': User's unique username.
    - 'email': User's unique email address.
    - 'profile_image_url': URL of the user's profile image.
    - 'id': Unique identifier (UUID) for the user.
    - 'user_role' : role of user.
    """

    pass


class UserCreate(
    UserBase,
    UserMediaBase,
    UserRoleBase,
):
    """
    API Schema

    Description:
    ----------
    Schema for creating a new user.

    Fields:
    ----------
    - 'name': User's full name.
    - 'username': User's unique username.
    - 'email': User's unique email address.
    - 'password': User's password.
    """

    model_config = ConfigDict(extra="forbid")  # type: ignore

    password: Annotated[
        str,
        Field(
            default="Pass@123",
            pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$",
            examples=["Str1ngst!"],
        ),
    ]


class UserCreateInternal(UserBase, UserMediaBase, UserRoleBase, UserSecurityBase):
    """
    API Schema

    Description:
    ----------
    Internal schema for creating a new user, including security information.

    Fields:
    ----------
    - 'name': User's full name.
    - 'username': User's unique username.
    - 'email': User's unique email address.
    - 'hashed_password': Hashed password for user authentication.
    """

    pass


@optional()
class UserUpdate(
    UserBase,
    UserMediaBase,
    UserRoleBase,
):
    """
    API Schema

    Description:
    ----------
    Schema for updating an existing user, including media information.

    Optional Fields:
    ----------
    - 'name': User's full name.
    - 'username': User's unique username.
    - 'email': User's unique email address.
    - 'profile_image_url': URL of the user's profile image.
    - 'user_role' : User role
    """

    model_config = ConfigDict(extra="forbid")  # type: ignore


class UserUpdateInternal(UserUpdate):
    """
    API Schema

    Description:
    ----------
    Internal schema for updating an existing user, including media information and the last update timestamp.

    Fields:
    ----------
    - 'name': User's full name.
    - 'username': User's unique username.
    - 'email': User's unique email address.
    - 'profile_image_url': URL of the user's profile image.
    - 'updated_at': Timestamp for the last update of the user record.
    """

    updated_at: datetime


class UserDelete(SoftDeleteMixin):
    """
    API Schema

    Description:
    ----------
    Schema for logically deleting a user.

    Fields:
    ----------
    - 'is_deleted': Flag indicating whether the user record is deleted (soft deletion).
    """

    model_config = ConfigDict(extra="forbid")  # type: ignore


class UserRestoreDeleted(BaseModel):
    """
    API Schema

    Description:
    ----------
    Schema for restoring a deleted user.

    Fields:
    ----------
    - 'is_deleted': Flag indicating whether the user record is deleted (soft deletion).
    """

    is_deleted: bool

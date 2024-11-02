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
from app.db.models.v1.db_address import UserAddress


class UserPersonalInfoBase(Base):
    """
    SQLModel Base

    Description:
    ----------
    'UserPersonalInfoBase' pydantic class with personal information for a user.

    Fields:
    ----------
    - 'name': User's full name.
    - 'username': User's unique username.
    - 'email': User's unique email address.
    - 'phone': User's unique phone number.

    Examples:
    ----------
    Examples of valid data for each field:
    - 'name': "Harsh Mittal"
    - 'username': "hm"
    - 'email': "harshmittal2210@gmail.com"
    - 'phone': "+919876543210"
    """

    # Data Columns
    name: str = Field(
        min_length=2,
        max_length=100,
        nullable=False,
        description="User's full name",
        schema_extra={"examples": ["Test User"]},
    )
    username: str = Field(
        min_length=2,
        max_length=20,
        unique=True,
        index=True,
        nullable=False,
        regex=r"^[a-z0-9]+$",
        description="User's username",
        schema_extra={"examples": ["test"]},
    )
    email: str = Field(
        max_length=50,
        unique=True,
        index=True,
        nullable=False,
        regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        description="User's email address",
        schema_extra={"examples": ["test@example.com"]},
    )  # Todo: Use EmailStr when it's supported by SQLModel (https://github.com/tiangolo/sqlmodel/pull/762)

    phone: str = Field(
        unique=True,
        index=True,
        nullable=False,
        regex=r"^\+?[1-9]\d{1,14}$",
        description="Phone number in international format, e.g., +919876543210",
        schema_extra={"examples": ["+919876543210"]},
    )


class UserMediaBase(Base):
    """
    SQLModel Base

    Description:
    ----------
    'UserMediaBase' pydantic class with media-related information for a user.

    Fields:
    ----------
    - 'profile_image_url': URL of the user's profile image.

    Examples:
    ----------
    Example of a valid data:
    - 'profile_image_url': "https://www.imageurl.com/profile_image.jpg"
    """

    # Data Columns
    profile_image_url: str = Field(
        default=f"{settings.DEFAULT_USER_IMAGE}",
        description="URL of the user's profile image",
        schema_extra={"examples": [settings.DEFAULT_USER_IMAGE]},
    )


class UserPermissionBase(Base):
    """
    SQLModel Base

    Description:
    ----------
    'UserPermissionBase' pydantic class with permission-related information for a user.

    Fields:
    ----------
    - 'is_superuser': Indicates whether the user has superuser privileges.

    Examples:
    ----------
    Example of a valid data:
    - 'is_superuser': False
    """

    # Data Columns
    is_superuser: bool = Field(
        default=False, description="Indicates whether the user has superuser privileges"
    )


class UserSecurityBase(Base):
    """
    SQLModel Base

    Description:
    ----------
    'UserSecurityBase' pydantic class with security-related information for a user.

    Fields:
    ----------
    - 'hashed_password': Hashed password for user authentication.

    Examples:
    ----------
    Example of a valid data:
    - 'hashed_password': "hashed_password_value"
    """

    # Data Columns
    hashed_password: str = Field(
        nullable=False, description="Hashed password for user authentication"
    )


class AccessLevel_Enum(str, Enum):
    """
    User Role Enum
    """

    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"
    MODERATOR = "moderator"


class UserRoleBase(Base):
    """
    Pydantic Base Model for User Role

    Attributes:
    ----------
    - user_role (AccessLevel_Enum): Role of the user.
        Examples:
        - admin: ADMIN
    """

    user_role: AccessLevel_Enum = Field(
        default=AccessLevel_Enum.GUEST.value,
        description="Role of the user.",
        schema_extra={"Examples": AccessLevel_Enum.GUEST.value},
    )


class UserDeliveryAddress(Base):
    delivery_addresses: List["UserAddress"] = Relationship(back_populates="customer")


# class UserPaymentMethods(Base):
#     payment_details: List["PaymentDetail"] = Relationship(back_populates="customer")

# class UserOrderList(Base):
#     orders: List["Order"] = Relationship(back_populates="customer")


class User(
    UserPersonalInfoBase,
    UserMediaBase,
    UserPermissionBase,
    UserSecurityBase,
    UserRoleBase,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    table=True,
):
    """
    SQLModel Table: User

    Description:
    ----------
    'User' ORM class representing the 'system_user' database table.

    Fields:
    ----------
    - 'name': User's full name.
    - 'username': User's unique username.
    - 'email': User's unique email address.
    - 'phone': User's unique phone number.
    - 'profile_image_url': URL of the user's profile image.
    - 'is_superuser': Indicates whether the user has superuser privileges.
    - 'hashed_password': Hashed password for user authentication.
    - 'id': Unique identifier (UUID) for the user.
    - 'created_at': Timestamp for the creation of the user record.
    - 'updated_at': Timestamp for the last update of the user record.
    - 'deleted_at': Timestamp for the deletion of the user record (soft deletion).
    - 'is_deleted': Flag indicating whether the user record is deleted (soft deletion).
    - 'user_role' : role of user.
    - 'sessions': list of all session of user
    Relationships:
    ----------

    Table Name:
    ----------
    'system_user'
    """

    __tablename__ = f"{settings.DATABASE_USER_TABLE}"

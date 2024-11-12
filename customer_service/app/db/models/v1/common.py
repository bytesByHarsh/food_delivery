# Built-in Dependencies
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Optional, Any
from enum import Enum, IntEnum


# Third-Party Dependencies
from sqlmodel import SQLModel, Field, DateTime
from pydantic import field_serializer


# Define a base class for declarative models with support for dataclasses
class Base(SQLModel):
    """
    SQLModel Base

    Description:
    ----------
    Main base class for generating Pydantic models and database tables with SQLModel.
    """

    pass


class UUIDMixin(SQLModel):
    """
    SQLModel Base

    Description:
    ----------
    'UUIDMixin' pydantic class with a UUID column as the primary key.

    Fields:
    ----------
    - 'id': Unique identifier (UUID) for the record.

    Examples:
    ----------
    Example of a valid data:
    - 'id': UUID("123e4567-e89b-12d3-a456-426614174001")
    """

    # Data Columns
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        description="Unique identifier (UUID) for the record",
    )


class TimestampMixin(SQLModel):
    """
    SQLModel Base

    Description:
    ----------
    'TimestampMixin' pydantic class.

    Fields:
    - 'created_at': Timestamp for the creation of the record.
    - 'updated_at': Timestamp for the last update of the record.

    Examples:
    ---------
    Examples of valid data for each field:
    - 'created_at': "2024-01-20T12:00:00"
    - 'updated_at': "2024-01-20T12:30:00"

    Extra Info:
    ----------
    Adds 'created_at' and 'updated_at' fields with default values for the creation timestamp and update timestamp.

    Note: By default, 'updated_at' is set to the current timestamp on every update, which is useful for tracking the last
    modification time. However, in scenarios where soft deletion is performed and records may be restored, you might want
    to consider the following options:

    ----------------------------------------------------------

    Option 1 (Recommended for most scenarios):
    - Pros:
        - Keeps 'updated_at' always up-to-date, providing an accurate timestamp for the last modification.
        - Suitable for most use cases where soft deletion is not a common scenario.

    - Cons:
        - May lead to inaccurate information if soft deletion and restoration are part of the system's workflow.

    updated_at: datetime = Field(
        sa_type=DateTime(timezone=True),
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={"onupdate": datetime.now(UTC)},
        description="Timestamp for the last update of the record",
    )

    ----------------------------------------------------------

    Option 2 (Recommended for scenarios with frequent soft deletions and restorations):
    - Pros:
        - Preserves the original timestamp of the last real modification even after a soft delete and restore.
        - Avoids potential inaccuracies caused by automatic updates to 'updated_at' during soft deletions.

    - Cons:
        - 'updated_at' will not be automatically updated on every change, potentially affecting accuracy if the field
        needs to reflect every modification.
        - Currently, the BaseCRUD's update method in the API automatically handles the update of 'updated_at'. If other
        update methods are used that do not go through this mechanism, 'updated_at' may not be updated as expected.

    updated_at: Optional[datetime] = Field(
        sa_type=DateTime(timezone=True),
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp for the last update of the record",
    )
    """

    # Data Columns
    created_at: datetime = Field(
        sa_type=DateTime(timezone=True),
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp for the creation of the record",
    )  # type: ignore
    updated_at: datetime = Field(
        sa_type=DateTime(timezone=True),
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": datetime.now(timezone.utc)},
        description="Timestamp for the last update of the record",
    )  # type: ignore

    @field_serializer("created_at")
    def serialize_dt(self, created_at: datetime, _info: Any) -> str:
        if created_at is not None:
            return created_at.isoformat()

        return None

    @field_serializer("updated_at")
    def serialize_updated_at(self, updated_at: datetime, _info: Any) -> str:
        if updated_at is not None:
            return updated_at.isoformat()

        return None


class SoftDeleteMixin(SQLModel):
    """
    SQLModel Base

    Description:
    ----------
    'SoftDeleteMixin' pydantic class.

    Fields:
    - 'deleted_at': Timestamp for the deletion of the record (soft deletion).
    - 'is_deleted': Flag indicating whether the record is deleted (soft deletion).

    Examples:
    ---------
    Examples of valid data for each field:
    - 'deleted_at': "2024-01-20T13:00:00"
    - 'is_deleted': True

    Extra Info:
    ----------
    Adds 'deleted_at' and 'is_deleted' fields for soft deletion functionality.
    """

    # Data Columns
    deleted_at: Optional[datetime] = Field(
        sa_type=DateTime(timezone=True),
        default=None,
        description="Timestamp for the deletion of the record (soft deletion)",
    )  # type: ignore
    is_deleted: bool = Field(
        default=False,
        index=True,
        description="Flag indicating whether the record is deleted (soft deletion)",
    )

    @field_serializer("deleted_at")
    def serialize_dates(self, deleted_at: datetime, _info: Any) -> str:
        if deleted_at is not None:
            return deleted_at.isoformat()

        return None


class Transaction_Status_Enum(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    IN_PROGRESS = "in-Progress"
    HOLD = "hold"
    IN_REVIEW = "in-review"
    REQUEST = "request"


class TransactionStatus(Base):
    status: Transaction_Status_Enum = Field(
        nullable=False,
        description="Status Enum for transactions",
        schema_extra={"examples": [f"{Transaction_Status_Enum.REQUEST.value}"]},
    )

    msg: str | None = Field(
        nullable=True,
        description="Any information related to transactions",
        default_factory=None,
    )


class Rating_enum(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
# Built-in Dependencies
from datetime import datetime

# Third-Party Dependencies
from sqlmodel import Field

# Local Dependencies
from app.db.models.v1.common import TimestampMixin, UUIDMixin, Base


class TokenBlacklistBase(Base):
    """
    SQLModel Base

    Description:
    ----------
    'TokenBlacklistBase' pydantic class with information about blacklisted tokens.

    Fields:
    ----------
    - 'token': Token value for authentication.
    - 'expires_at': Timestamp indicating the expiration date and time of the token.

    Examples:
    ----------
    Examples of valid data for each field:
    - 'token': "example_token_value"
    - 'expires_at': "2024-01-20T12:00:00"

    Note: The 'expires_at' field should be provided in ISO 8601 format.
    """

    # Data Columns
    token: str = Field(
        index=True,
        nullable=False,
        default=None,
        description="Token value for authentication",
    )
    expires_at: datetime = Field(
        nullable=False,
        default=None,
        description="Timestamp indicating the expiration date and time of the token",
    )  # type: ignore


class TokenBlacklist(TokenBlacklistBase, UUIDMixin, TimestampMixin, table=True):
    """
    SQLModel Table

    Description:
    ----------
    'TokenBlacklist' ORM class representing the 'system_token_blacklist' database table.

    Fields:
    ----------
    - 'token': Token value for authentication.
    - 'expires_at': Timestamp indicating the expiration date and time of the token.
    - 'id': Unique identifier (UUID) for the token blacklist entry.
    - 'created_at': Timestamp for the creation of the token blacklist entry.
    - 'updated_at': Timestamp for the last update of the token blacklist entry.

    Table Name:
    ----------
    'system_token_blacklist'
    """

    __tablename__ = "system_token_blacklist"

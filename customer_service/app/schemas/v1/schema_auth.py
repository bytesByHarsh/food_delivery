from pydantic import BaseModel

# Local Dependencies
from app.db.models.v1.db_auth import TokenBlacklistBase
from app.utils.partial import optional


class Token(BaseModel):
    """
    API Schema

    Description:
    ----------
    Response schema for representing a token.

    Fields:
    ----------
    - 'access_token' (str): The access token.
    - 'token_type' (str): The type of the token.
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    API Schema

    Description:
    ----------
    Response schema for representing token data.

    Fields:
    ----------
    - 'username_or_email' (str): The username or email associated with the token.
    """

    username_or_email: str


class TokenBlacklistCreate(TokenBlacklistBase):
    """
    API Schema

    Description:
    ----------
    Schema for creating a token blacklist entry.

    Fields:
    ----------
    - 'token': Token value for authentication.
    - 'expires_at': Timestamp indicating the expiration date and time of the token.
    """

    pass


# All these fields are optional
@optional()
class TokenBlacklistUpdate(TokenBlacklistBase):
    """
    API Schema

    Description:
    ----------
    Schema for updating a token blacklist entry.

    Optional Fields:
    ----------
    - 'token': Token value for authentication.
    - 'expires_at': Timestamp indicating the expiration date and time of the token.
    """

    pass

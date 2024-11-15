from typing import Optional, Dict, Literal, Union, Any
from datetime import datetime, timedelta, timezone


# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuthFlowPassword
from fastapi import Request, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt, JWTError


# Local Dependencies
from app.core.config import settings
from app.schemas.v1.schema_auth import TokenData, TokenBlacklistCreate
from app.db.crud.crud_auth import crud_token_blacklist
from app.db.crud.crud_restaurant import crud_restaurants, get_restaurant
from app.core.hashing import Hasher


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}

        flows = OAuthFlowsModel(
            password=OAuthFlowPassword(tokenUrl=tokenUrl, scopes=scopes)
        )
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str | None = request.cookies.get("access_token")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/auth/login")


# Function to authenticate a user based on provided credentials
async def authenticate_user(
    username_or_email: str, password: str, db: AsyncSession
) -> Union[Dict[str, Any], Literal[False]]:
    db_user = await get_restaurant(username_or_email, db)

    if not db_user:
        return False

    elif not Hasher.verify_password(password, db_user["hashed_password"]):
        return False

    return db_user


async def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc).replace(tzinfo=None) + expires_delta
    else:
        expire = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


# Function to create a refresh token with optional expiration time
async def create_refresh_token(
    data: Dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc).replace(tzinfo=None) + expires_delta
    else:
        expire = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(
            days=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


# Function to verify the validity of a token and return TokenData if valid
async def verify_token(token: str, db: AsyncSession) -> TokenData | None:
    """
    Verify a JWT token and return TokenData if valid.

    Parameters
    ----------
    token: str
        The JWT token to be verified.
    db: AsyncSession
        Database session for performing database operations.

    Returns
    ----------
    TokenData | None
        An instance of TokenData representing the user if the token is valid.
        None is returned if the token is invalid or the user is not active.
    """
    is_blacklisted = await crud_token_blacklist.exists(db, token=token)
    if is_blacklisted:
        return None

    try:
        # Decode the token payload and extract the subject (username or email)
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username_or_email: str | None = payload.get("sub")
        if username_or_email is None:
            return None

        # Check if the Redis client is available
        # if cache.client:
        #     # Check if user is active in Redis
        #     is_active = await cache.client.hget(
        #         settings.REDIS_HASH_SYSTEM_AUTH_VALID_USERNAMES,
        #         username_or_email,
        #     )

        #     if is_active:
        #         return TokenData(username_or_email=username_or_email)

        # If not active in Redis or Redis is not available, check PostgreSQL
        user = await crud_restaurants.get(db=db, username=username_or_email, is_deleted=False)

        if user:
            # Update Redis with user active status if Redis is available
            # if cache.client:
            #     await cache.client.hset(
            #         settings.REDIS_HASH_SYSTEM_AUTH_VALID_USERNAMES,
            #         username_or_email,
            #         "active",
            #     )

            return TokenData(username_or_email=username_or_email)

        # If user is not found in Redis or PostgreSQL, blacklist the token
        await blacklist_token(token=token, db=db)

        return None

    except JWTError:
        return None


# Function to blacklist a token by storing it in the database
async def blacklist_token(token: str, db: AsyncSession) -> None:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    expires_at = datetime.fromtimestamp(payload.get("exp", 0.0))
    await crud_token_blacklist.create(
        db,
        object=TokenBlacklistCreate(**{"token": token, "expires_at": expires_at}),
    )
